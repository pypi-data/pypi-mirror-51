
"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from functools import lru_cache
from cortex_profiles.schemas.schemas import CONTEXTS
import base64
from typing import List, Optional, Tuple, Callable, Any, Mapping

import attr
import jwt
import pydash
import pymongo

from cortex_client import _Client, AuthenticationClient, SecretsClient
from cortex_profiles import utils, queries, profile_commit_utils
from cortex_profiles.profile_commit_utils import apply_commits_onto_profile, profile_commit_chain_from_recursive_commit
from cortex_profiles.profile_commit_utils import determine_attribute_modification_deltas_relevant_to_profile
from cortex_profiles.schemas.schemas import UNIVERSAL_ATTRIBUTES
from cortex_profiles.types.attributes import BaseProfileAttribute, ProfileAttribute
from cortex_profiles.types.attributes import load_profile_attribute_from_dict
from cortex_profiles.types.general import AggregateQuery, OrderedList
from cortex_profiles.types.internal import LatestCommitPointer
from cortex_profiles.types.profiles import ProfileCommit, Profile, ProfileSnapshot, ProfileSummary
from cortex_profiles.types.schema import ProfileSchema
from cortex_profiles.types.api import DeleteProfileResponse
from cortex_profiles.utils import group_objects_by


class InternalProfilesClient(_Client):
    """A client for the Cortex Profiles SDK Functionality."""


    def __init__(self, url:str, version:str, token:str, environmentId:str="cortex/default", mongodb_factory:Optional[Callable[[], Any]]=None):
        self.token = token

        # Parse Tenant from token ...
        self.tenantId = jwt.decode(token, verify=False)["tenant"]
        self.environmentId = environmentId

        # databases here ...
        self.mongodb = mongodb_factory() if mongodb_factory else pymongo.MongoClient(self.get_mongo_db_secret(url))["cortex-graph"]

        self.latest_commit_pointers_collection = self.mongodb["commit-pointers"]
        self.commits_collection = self.mongodb["commits"]
        self.snapshots_collection = self.mongodb["snapshots"]
        self.attributes_collection = self.mongodb["attributes"]
        self.schemas_collection = self.mongodb["schemas"]

    def get_mongo_db_secret(self, url:str) -> str:
        self.secretsclient = SecretsClient(url, "2", self.token)
        self.authclient = AuthenticationClient(url, "2", self.token)
        # Verfiy its a valid token ...
        self.authclient.refresh_token()
        secret = self.secretsclient.get_secret(base64.b64decode(b'ZnBp').decode("utf-8"))
        if not secret:
            raise Exception("Failed to get secret.")
        return secret.get("mongo_uri", None)

    def index_databases(self):
        from pymongo import IndexModel, ASCENDING, DESCENDING

        index_id = IndexModel([("id", ASCENDING), ("createdAt", DESCENDING)], name="id_with_time")
        index_environ = IndexModel([("environmentId", ASCENDING)], name="environment_parition")
        index_tenant = IndexModel([("tenantId", ASCENDING)], name="tenant_partition")

        base_indexes = [index_id, index_environ, index_tenant]
        self.schemas_collection.create_indexes(base_indexes)

        index_profile = IndexModel([("profileId", ASCENDING)], name="profileId_asc")
        self.latest_commit_pointers_collection.create_indexes(base_indexes + [index_profile])
        self.snapshots_collection.create_indexes(base_indexes + [index_profile])
        self.commits_collection.create_indexes(base_indexes + [index_profile])

        index_attr_key = IndexModel([("attributeKey", ASCENDING)], name="attrkey_asc")
        self.attributes_collection.create_indexes(base_indexes + [index_profile, index_attr_key])

    def flush_databases(self):
        self.latest_commit_pointers_collection.drop()
        self.commits_collection.drop()
        self.snapshots_collection.drop()
        self.attributes_collection.drop()
        self.schemas_collection.drop()
        # self.profiles_collection.drop()
        # self.locks_collection.drop()

    def flush_collection(self, collection):
        return collection.delete_many(self.append_secure_variables_to_query({}))

    def flush_profiles(self):
        self.flush_collection(self.latest_commit_pointers_collection)
        self.flush_collection(self.commits_collection)
        self.flush_collection(self.snapshots_collection)
        self.flush_collection(self.attributes_collection)
        # self.flush_collection(self.profiles_collection)
        # self.flush_collection(self.locks_collection)

    @utils.timeit
    def append_attributes_to_profile(
            self,
            attributes: List[ProfileAttribute],
            profileId: str
        ) -> Tuple[Profile, ProfileCommit]:
        """
        :param attributes: List of Profile Attributes we want to push to the profile ...
        :param profileId:  The id of the profile we want to update (do we actually need this? ... isn't this in the attribute? ...)
        :return:
        """

        # when an attribute is saved ... save it with the commit that it was created in?
        #     when a new commit happens,
        #         update all the attributes associated with the old commit to be associated with the new commit ...
        #     Get all of the attributes if specified ... else ... get the list specified ...

        # Get latest Commit ... or Create a new one if it doesnt exist ...
        default_commit = self.default_commit_for_user(profileId)
        latest_commit = self.find_latest_commit_for_profile_or_create(profileId, default_commit)

        # Get Profile from latest commit
        latest_profile = self.get_profile_based_off_commitId(profileId, latest_commit.id)

        # append appropriate env and tenant to profile attributes ...
        attributes = [attr.evolve(a, tenantId=self.tenantId, environmentId=self.environmentId) for a in attributes]

        # Figure out which attributes are new ... modified ... removed ...
        attrs_added, attrs_modified, attrs_removed = determine_attribute_modification_deltas_relevant_to_profile(
            attributes, latest_profile)

        # Derive new commit from latest commit + attribute modifications
        new_commit = profile_commit_utils.extend_commit_with_attributes(
            latest_commit, attrs_added, attrs_modified, attrs_removed)

        # Save newest commit
        saved_commit = self.save_profile_commit(new_commit)
        # helpers.print_attr_class_with_header("saved_commit: ", saved_commit)

        # Save the newly attributes & the new valued for the modified attributes.
        #   Also decommission the old modified attributes
        saved_attributes = self.save_attributes(attributes, latest_commit, new_commit)

        # Update the pointer to the latest commit ... from the old commit to the new one ..
        latest_commit_pointer = self.update_latest_commit_pointer(latest_commit, new_commit)

        # Rebuild the latest profile from the latest commits ...
        latest_profile = self.get_latest_profile(profileId)

        # Expand the profile and save it as a snapshot to be queried ...
        expanded_profile = self.expand_profile(latest_profile)
        expanded_profile = self.replace_latest_snapshot_for_profile(expanded_profile)

        return latest_profile, saved_commit

    def unique_attribute_keys(self, query:Optional[dict]=None) -> Optional[Profile]:
        return self.attributes_collection.distinct(
            "attributeKey", self.append_secure_variables_to_query(pydash.merge({}, query if query else {}))
        )

    def get_profile(self, profileId:str, commitId:Optional[str]=None) -> Optional[Profile]:
        return (
            self.get_latest_profile(profileId)
           if not commitId else self.get_profile_based_off_commitId(profileId, commitId)
        )

    def get_commit_history_for_profile(self, profileId:str) -> OrderedList[ProfileCommit]:
        return list(map(
            lambda x: ProfileCommit(**x),
            self.commits_collection.find(
                self.append_secure_variables_to_query({"profileId": profileId}),
                {"_id": 0}
            ).sort([("createdAt", -1)])
        ))

    def get_commit_by_id(self, commitId:str) -> Optional[ProfileCommit]:
        commit = self.commits_collection.find_one(
            self.append_secure_variables_to_query({
                "id": commitId
            }),
            {"_id": 0}
        )
        return ProfileCommit(**commit) if commit else None

    def get_attribute_by_id(self, attributeId:str) -> Optional[ProfileAttribute]:
        attribute = self.attributes_collection.find_one(
            self.append_secure_variables_to_query({
                "id": attributeId
            }),
            {"_id": 0}
        )
        return load_profile_attribute_from_dict(attribute) if attribute else None

    def get_attribute_by_key(self, profileId:str, attributeKey:str, commitId:str) -> Optional[ProfileAttribute]:
        attribute = self.attributes_collection.find_one(
            self.append_secure_variables_to_query({
                "profileId": profileId,
                "attributeKey": attributeKey,
                "commits": commitId
            }),
            {"_id": 0}
        )
        return load_profile_attribute_from_dict(attribute) if attribute is not None else None

    def get_latest_attributes_for_profile(self, profileId: str, attributesKeys: List[str]) -> List[ProfileAttribute]:
        # snapshot = find_latest_snapshot_for_profile(profileId, cortex)
        # attributes = snapshot.attributes if snapshot else []
        # Todo ... inefficient ... we get the whole profile ... them manually filter what we dont want ...
        # Can we get only what we want?
        # At the same time ... we only want to query amoungst the latest attributes ... (should we get latest commitid first?)
        # return attributes if not attributesKeys else list(filter(
        #     lambda attr: attr.attributeKey in attributesKeys,
        #     attributes
        # ))
        return self.find_latest_attributes_for_profile(profileId, attributesKeys)

    def get_latest_profile_commit(self, profileId:str) -> Optional[ProfileCommit]:
        """
        Getting the latest commit is like getting any other commit ...
        Where as searching ... is done on the most up to date attributes ...

        :param profileId:
        :return:
        """
        # TODO Add branches ...
        latest_commit = self.latest_commit_pointers_collection.find_one(
            self.append_secure_variables_to_query({"profileId": profileId}),
            {"_id": 0}
            # Don't need to sort because only 1 pointer should exist per profile
        )

        latest_commit_pointer = LatestCommitPointer(**latest_commit) if latest_commit else None
        if not latest_commit_pointer:
            return None
        return self.get_commit_by_id(latest_commit_pointer.commitId)


    def get_latest_profile(self, profileId:str) -> Optional[Profile]:
        """
        Gets the latest profile for the specified profile id.
        :param profileId:
        :return:
        """
        commit = self.get_latest_profile_commit(profileId)
        # helpers.print_attr_class_with_header("Latest profile commit: ", commit)
        if not commit:
            return None
        return self.get_profile_based_off_commitId(profileId, commit.id)

    def get_profile_based_off_commitId(self, profileId: str, commitId:str) -> Profile:
        """
        Builds the latest profile starting at the specified commit, recursively.
        :param commitId:
        :return:
        """
        commits = self.find_commits_recursively_starting_from(profileId, commitId)
        # Build profile from recursive commits ...
        return self.build_profile_from_commits(list(reversed(commits)), commitId, profileId)

    def expand_profile(self, profile:Profile) -> Optional[ProfileSnapshot]:
        if profile is not None:
            return ProfileSnapshot(
                **utils.merge_dicts(
                    attr.asdict(profile),
                    {
                        "attributes": self.get_attributes_associated_with_profile(profile),
                        "context": attr.fields(ProfileSnapshot).context.default
                    }
                )
            )
        else:
            return None

    def sort_counter_based_attributes(self, attributeKey:str, pick:int=5, ascending=True) -> List[dict]:
        """
        This queries a specific attribute across

        One of the reason we wanted onLatestProfile ... was to be able to do things like top 5 ... for a counter across all users ...
        We effectively want a find latest attribute for all users ...

        TODO .... Can we maintain a seperate collection that states what are all the latest attributes ...?

        :param attributeKey:
        :param pick:
        :param ascending:
        :return:
        """

        return list(map(
            lambda x: utils.drop_from_dict(x, ["_id"]),
            self.attributes_collection.find(
                self.append_secure_variables_to_query({
                    "onLatestProfile": True,
                    "attributeKey": attributeKey,
                    "attributeValue.context": CONTEXTS.COUNTER_PROFILE_ATTRIBUTE_VALUE

                })
            ).sort([("attributeValue.value", -1 if not ascending else 1)]).limit(pick)
        ))

    def build_profile_from_commits(self, commits:OrderedList[ProfileCommit], commitId:str, profileId:str) -> Optional[Profile]:
        if not commits:
            return None
        # helpers.print_attr_class_with_header("Applying commits", commits)
        return apply_commits_onto_profile(
            commits,
            self.default_profile_for_user(profileId, commitId)
        )

    def dervive_latest_commit_pointer_from_commit(self, commit:ProfileCommit) -> LatestCommitPointer:
        return LatestCommitPointer(
            id=utils.unique_id(),
            commitId=commit.id,
            profileId=commit.profileId,
            environmentId=self.environmentId,
            tenantId=self.tenantId,
            createdAt=utils.utc_timestamp()
        )

    def default_profile_for_user(self, profileId: str, commitId:str) -> Profile:
        return Profile(
            id=profileId,
            commitId=commitId,
            createdAt=utils.utc_timestamp(),
            tenantId=self.tenantId,
            environmentId=self.environmentId
        )

    def default_commit_for_user(self, profileId: str) -> ProfileCommit:
        return ProfileCommit(
            id=utils.unique_id(),
            createdAt=utils.utc_timestamp(),
            profileId=profileId,
            tenantId=self.tenantId,
            environmentId=self.environmentId
        )

    def find_profiles(self, query: dict) -> List[ProfileSnapshot]:
        # Limit Scope of Query ...
        restricted_query = queries.append_leaf_queries_with(
            query,
            self.append_secure_variables_to_query({})
       )
        # helpers.print_json_with_header("Query to run", restricted_query)
        # Find snapshots ...
        return list(map(
            ProfileSnapshot.from_dict,
            self.snapshots_collection.find(
                restricted_query,
                {"_id": 0}
            )
        ))

    def query_latest_attributes(self, query: dict, query_options: dict) -> object:
        return self.attributes_collection.find(
            queries.append_leaf_queries_with(query, self.append_secure_variables_to_query({})),
            **query_options
        )

    @lru_cache(maxsize=100)
    def list_of_attributeIds_in_profile(self, profileId:str, commitId:str) -> Optional[List[str]]:
        """
        Returns a list of all the attributesIds present in a profile.
        Cachable since list of attributes in profile should never change.

        :param profileId:
        :param commitId:
        :return: List of all commit ids after all the commits are recursively applied to the profile ...
        """
        profile_at_commit = self.get_profile_based_off_commitId(profileId, commitId)
        if profile_at_commit is None:
            return None
        return list(map(lambda x : x.attributeId, profile_at_commit.attributes))

    def find_latest_attributes_for_profile(self, profileId: str, attributeKeys: Optional[str]) -> List[ProfileAttribute]:
        query = self.append_secure_variables_to_query({
            "onLatestProfile": True,
            "profileId": profileId
        })
        if attributeKeys:
            query["attributeKey"] = {
                "$in": attributeKeys
            }
        return list(map(
            load_profile_attribute_from_dict,
            self.attributes_collection.find(query, {"_id": 0})
        ))

    def find_latest_commit_for_profile_or_create(self, profileId:str, default_commit:ProfileCommit) -> ProfileCommit :
        """
        Finds the latest commit on a specific profile id. It starts by looking for a pointer to the latest commit for a profile.
        If not commit is found it creates a default commit and creates a new pointer that points to the default commit.
        :param profileId:
        :param default_commit:
        :param cortex:
        :return:
        """

        # First ... find the latest pointer or create it ...
        pointer = LatestCommitPointer(
            **utils.drop_from_dict(
                queries.find_or_create_atomically(
                    self.latest_commit_pointers_collection,
                    self.append_secure_variables_to_query({
                        "profileId": profileId
                    }),
                    attr.asdict(self.dervive_latest_commit_pointer_from_commit(default_commit)),
                    {
                        "sort": [('createdAt', pymongo.DESCENDING)],
                        "upsert": True,
                        "return_document": pymongo.ReturnDocument.AFTER
                    }
                ),
                ["_id"]
            )
        )

        # Then ... find the latest commit from the pointer (or create the default commit if it doesn't exist)
        commit = queries.find_or_create_atomically(
            self.commits_collection,
            self.append_secure_variables_to_query({
                "id": pointer.commitId,
                "profileId": pointer.profileId
            }),
            attr.asdict(default_commit),
            {
                "sort": [('createdAt', pymongo.DESCENDING)],
                "upsert": True,
                "return_document": pymongo.ReturnDocument.AFTER
            }
        )
        return ProfileCommit(**utils.drop_from_dict(commit, ["_id"]))

    def save_profile_commit(self, commit: ProfileCommit) -> ProfileCommit:
        safe_commit = utils.modify_attr_class(commit, self.append_secure_variables_to_query({}))
        saved_commit = self.commits_collection.find_one_and_replace(
            {"id": safe_commit.id},
            attr.asdict(safe_commit),
            **{
                "upsert": True,
                "return_document": pymongo.ReturnDocument.AFTER
            }
        )
        return ProfileCommit(**utils.drop_from_dict(saved_commit, ["_id"]))

    def find_commits_recursively_starting_from(self, profileId: str, commitId:str) -> List[ProfileCommit]:
        """
        This returns a list of commits, starting with the newest one first ...
        :param commitId:
        :return:
        """
        query_results = list(self.commits_collection.aggregate(self.build_query_commits_recursively(profileId, commitId)))
        recursive_commit  = utils.drop_from_dict(query_results[0], ["_id"]) if query_results else []
        # helpers.print_json_with_header("Recursive commit starting at {}".format(commitId), recursive_commit)
        # Derive a list of all the commits in cronological order ...
        return profile_commit_chain_from_recursive_commit(recursive_commit)

    def build_query_commits_recursively(self, profileId: str, commitId:str) -> AggregateQuery:
        return [
            {
                "$match": self.append_secure_variables_to_query({
                  "id": commitId,
                  "profileId": profileId
                })
            },
            # Find all of the commits that this commit is chained to ...
            {
                "$graphLookup" : {
                    "from": self.commits_collection.name,
                    "startWith": '$extends',
                    "connectFromField": 'extends',
                    "connectToField": 'id',
                    "as": 'recursive_commits',
                    "restrictSearchWithMatch": self.append_secure_variables_to_query({})
                }
            }
        ]

    def replace_latest_snapshot_for_profile(self, snapshot:ProfileSnapshot) -> ProfileSnapshot:
        return utils.drop_from_dict(
            self.snapshots_collection.find_one_and_replace(
                self.append_secure_variables_to_query({
                    "id": snapshot.id
                }),
                attr.asdict(snapshot),
                **{
                    "upsert": True,
                    "return_document": pymongo.ReturnDocument.AFTER
                }
            ), ["_id"]
        )

    def get_attributes_associated_with_profile(self, profile: Profile) -> List[ProfileAttribute]:
        data_for_raw_attributes = list(self.attributes_collection.find(
            self.append_secure_variables_to_query({
                "id": {"$in": [attribute.attributeId for attribute in profile.attributes]}
            })
        ))
        # print(data_for_raw_attributes) -> These are fine, theyre all Nones ...
        attributes = list(map(
            lambda x: load_profile_attribute_from_dict(utils.drop_from_dict(x, ["_id"])),
            data_for_raw_attributes
        ))
        # print(attributes)
        return attributes

    def update_latest_commit_pointer(self, fromCommit:ProfileCommit, toCommit:ProfileCommit) -> LatestCommitPointer:
        pointer = self.dervive_latest_commit_pointer_from_commit(toCommit)
        saved_pointer = self.latest_commit_pointers_collection.find_one_and_replace(
            self.append_secure_variables_to_query({
                "commitId": fromCommit.id,
                "profileId": fromCommit.profileId
            }),
            attr.asdict(pointer),
            **{
                "upsert": True,
                "return_document": pymongo.ReturnDocument.AFTER
            }
        )
        return utils.drop_from_dict(saved_pointer, ["_id"])

    def save_attributes(self, attributes: List[ProfileAttribute], oldCommit: ProfileCommit, newCommit: ProfileCommit) -> object:
        """
        Save new attributes ...
        Replace Modified attributes ...
        """
        operations = (
                queries.derive_operations_to_carry_over_uneffected_attributes_from_old_commit_to_new_commit(oldCommit, newCommit) +
                queries.derive_operations_to_save_new_attributes_and_associate_them_with_latest_commit(attributes, newCommit) +
                queries.derive_operations_to_save_modified_attributes_and_associate_them_with_latest_commit(attributes, newCommit) +
                queries.derive_operations_to_unmark_changed_attributes_as_latest(oldCommit, newCommit)
        )
        return utils.drop_from_dict(self.attributes_collection.bulk_write(operations).bulk_api_result, ["_id"])

    def counts_of_latest_attributes_per_profile(self, query:Optional[dict]=None) -> List[dict]:
        """
        Gives us a count of the number of attributes in the latest attributes in a specific profile ...
        :param query:
        :return:
        """
        query = utils.merge_dicts({} if not query else query, {
            "onLatestProfile": True
        })
        return list(map(
            lambda x: utils.merge_dicts(x["_id"], {"totalCountOfLatestAttributes": x["count"]}),
            self.attributes_collection.aggregate(
                [
                    {
                        "$match": self.append_secure_variables_to_query(query)
                    },
                    {
                        "$group": {
                            "_id": {"profileId": "$profileId", "profileType": "$profileType"},
                            "count": {
                                "$sum": 1
                            }
                        }
                    }
                ]
            )
        ))

    def count_of_profiles(self, query:Optional[dict]=None) -> Optional[int]:
        query = {} if query is None else query
        return self.snapshots_collection.count(self.append_secure_variables_to_query(query))

    # def list_profiles(self, query:Optional[dict]=None) -> List[ProfileSummary]:
    #     """
    #     This doesnt do too well if we decommission attributes ...
    #     :param query:
    #     :return:
    #     """
    #     return list(map(
    #         lambda x: ProfileSummary(**(x["_id"])),
    #         self.attributes_collection.aggregate(
    #             [
    #                 {
    #                     "$match": self.append_secure_variables_to_query({} if not query else query)
    #                 },
    #                 {
    #                     "$group": {
    #                         "_id": {"profileId": "$profileId", "profileType": "$profileType"},
    #                     }
    #                 }
    #             ]
    #         )
    #     ))

    def list_profiles(self, query:Optional[dict]={}) -> List[ProfileSnapshot]:
        return self.find_profiles(query)

    def list_profile_summaries(self, query:Optional[dict]={}, profileType:Optional[str]=None) -> List[ProfileSummary]:
        """
        This doesnt do too well if we decommission attributes ...
        :param query:
        :return:
        """

        if profileType is None:
            # Return all profiles ... whether they have a type or not ...

            types_for_profiles = {}
        else:

            profileAttrFields = attr.fields(BaseProfileAttribute)

            initial_profile_attribute_type_query = {} if profileType is None else {
                profileAttrFields.attributeKey.name: UNIVERSAL_ATTRIBUTES.TYPES,
                profileAttrFields.attributeValue.name: profileType
            }

            # Get all the profileIds of the profiles that have the profileType in its type list ...
            type_attributes = list(self.attributes_collection.find(
                self.append_secure_variables_to_query(initial_profile_attribute_type_query)
            ))
            # Get a list of all the profiles with that type ...
            types_for_profiles = {
                k: v[0] for k, v in group_objects_by(type_attributes, lambda x: x["profileId"]).items()
            }

            # Return only profiles of that types ...
            profiles = self.snapshots_collection.find(self.append_secure_variables_to_query(
                pydash.merge(
                    query,
                    {
                        profileAttrFields.profileId.name: {
                            "$in": list(types_for_profiles.keys())
                        }
                    }
                )
            ))

        # TODO .. append typeless profiles ...
        return list(map(
            lambda profileSnapshot: ProfileSummary(
                profileTypes=types_for_profiles.get(profileSnapshot["id"], {}).get("attributeValue", {"value":[]})["value"],
                profileId=profileSnapshot["id"],
                attributes=len(profileSnapshot["attributes"])
            ),
            profiles
        ))


    def find_attributes(self, attributeIds: List[str]) -> List[ProfileAttribute]:
        return list(map(
            lambda x: load_profile_attribute_from_dict(utils.drop_from_dict(x, ["_id"])),
            self.attributes_collection.find(
                self.append_secure_variables_to_query({
                    "id": {"$in": attributeIds}
                })
            )
        ))

    def find_latest_snapshot_for_profile(self, profileId: str) -> ProfileSnapshot:
        query = self.append_secure_variables_to_query({"id": profileId})
        # helpers.print_json_with_header("Query to run ... ", query)
        snapshot = pydash.rename(utils.drop_from_dict(self.snapshots_collection.find_one(query), ["_id"]), {"id": "profileId"})
        return ProfileSnapshot.from_dict(snapshot) if snapshot else None

    def list_schemas(self) -> List[ProfileSchema]:
        raw_schemas = list(self.schemas_collection.find(self.append_secure_variables_to_query({}), {"_id": 0}))
        schemas = [
            ProfileSchema(**utils.drop_from_dict(schema, ["_id"]))
            for schema in raw_schemas
        ]
        return schemas

    def get_schema(self, schemaId:str) -> Optional[ProfileSchema]:
        schema = self.schemas_collection.find_one({"id": schemaId})
        return ProfileSchema(**
            utils.drop_from_dict(schema, ["_id"])
        ) if schema is not None else None

    def upsert_profile_schema(self, schema:ProfileSchema) -> ProfileSchema:
        upsert_result = self.schemas_collection.replace_one(
            self.append_secure_variables_to_query({"id": schema.id}),
            pydash.merge(attr.asdict(schema), self.append_secure_variables_to_query({})),
            upsert=True
        )
        return self.get_schema(schema.id)

    def append_secure_variables_to_query(self, query:dict) -> dict:
        return utils.merge_dicts(query, {
            "environmentId": self.environmentId,
            "tenantId": self.tenantId,
        })

    def delete_profile(self, profileId:str) -> DeleteProfileResponse:
        # TODO ... recursively make sure the stuff we are deleting is not being used elsewhere ...
        from cortex_profiles.types.api import DeleteProfileResponse
        return DeleteProfileResponse(**{
            "snapshots_deleted": self.snapshots_collection.delete_many(self.append_secure_variables_to_query({"id": profileId})).deleted_count,
            "commit_pointers_deleted": self.latest_commit_pointers_collection.delete_many(self.append_secure_variables_to_query({"profileId": profileId})).deleted_count,
            "commits_deleted": self.commits_collection.delete_many(self.append_secure_variables_to_query({"profileId": profileId})).deleted_count,
            "attributes_deleted": self.attributes_collection.delete_many(self.append_secure_variables_to_query({"profileId": profileId})).deleted_count
        })

    def delete_schema(self, schemaId:str):
        return self.schemas_collection.delete_many(self.append_secure_variables_to_query({"id": schemaId}))

    def find_profiles_with_all_attributes(self, attribute_keys:List[str]) -> List[str]:
        query = self.append_secure_variables_to_query({
            "attributes": {
                "$all": [
                    {"$elemMatch": { "attributeKey": k } }
                    for k in attribute_keys
                ]
            }
        })
        return list(map(lambda x: x["id"], self.snapshots_collection.find(query, {"id": 1})))

    def find_profiles_with_none_of_the_attributes(self, attribute_keys:List[str]) -> List[str]:
        query = self.append_secure_variables_to_query({
            "attributes": {
                "$not": {
                    "$all": [
                        {"$elemMatch": {"attributeKey": k}}
                        for k in attribute_keys
                    ]
                }
            }
        })
        return list(map(lambda x: x["id"], self.snapshots_collection.find(query, {"id": 1})))

    def find_profiles_with_any_of_the_attributes(self, attribute_keys:List[str]) -> List[str]:
        query = self.append_secure_variables_to_query({
            "attributes": {
                "$elemMatch": {
                    "attributeKey": {"$in": attribute_keys}
                }
            }
        })
        return list(map(lambda x: x["id"], self.snapshots_collection.find(query, {"id": 1})))

    def find_profiles_updated_between(self, start_time:str, end_time:str):
        query = self.append_secure_variables_to_query({
            "$and": [
                {"createdAt": {"$gte": start_time}},
                {"createdAt": {"$lt": end_time}},
            ]
        })
        return list(self.commits_collection.find(query).distinct("profileId"))