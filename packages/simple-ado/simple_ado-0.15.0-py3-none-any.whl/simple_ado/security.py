#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""ADO security API wrapper."""

import enum
import json
import logging
from typing import ClassVar, Dict, List
import urllib.parse


from simple_ado.base_client import ADOBaseClient
from simple_ado.context import ADOContext
from simple_ado.exceptions import ADOException
from simple_ado.http_client import ADOHTTPClient, ADOResponse
from simple_ado.types import TeamFoundationId


class ADOBranchPermission(enum.IntEnum):
    """Possible types of git branch permissions."""

    ADMINISTER: int = 2 ** 0
    READ: int = 2 ** 1
    CONTRIBUTE: int = 2 ** 2
    FORCE_PUSH: int = 2 ** 3
    CREATE_BRANCH: int = 2 ** 4
    CREATE_TAG: int = 2 ** 5
    MANAGE_NOTES: int = 2 ** 6
    BYPASS_PUSH_POLICIES: int = 2 ** 7
    CREATE_REPOSITORY: int = 2 ** 8
    DELETE_REPOSITORY: int = 2 ** 9
    RENAME_REPOSITORY: int = 2 ** 10
    EDIT_POLICIES: int = 2 ** 11
    REMOVE_OTHERS_LOCKS: int = 2 ** 12
    MANAGE_PERMISSIONS: int = 2 ** 13
    CONTRIBUTE_TO_PULL_REQUESTS: int = 2 ** 14
    BYPASS_PULL_REQUEST_POLICIES: int = 2 ** 15


class ADOBranchPermissionLevel(enum.IntEnum):
    """Possible values of git branch permissions."""

    NOT_SET: int = 0
    ALLOW: int = 1
    DENY: int = 2


class ADOBranchPolicy(enum.Enum):
    """Possible types of git branch protections."""

    APPROVAL_COUNT: str = "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd"
    BUILD: str = "0609b952-1397-4640-95ec-e00a01b2c241"
    REQUIRED_REVIEWERS: str = "fd2167ab-b0be-447a-8ec8-39368250530e"
    CASE_ENFORCEMENT: str = "7ed39669-655c-494e-b4a0-a08b4da0fcce"
    MAXIMUM_BLOB_SIZE: str = "2e26e725-8201-4edd-8bf5-978563c34a80"
    MERGE_STRATEGY: str = "fa4e907d-c16b-4a4c-9dfa-4916e5d171ab"
    WORK_ITEM: str = "40e92b44-2fe1-4dd6-b3d8-74a9c21d0c6e"


class ADOSecurityClient(ADOBaseClient):
    """Wrapper class around the undocumented ADO Security APIs.

    :param context: The context information for the client
    :param http_client: The HTTP client to use for the client
    :param log: The logger to use
    """

    GIT_PERMISSIONS_NAMESPACE: ClassVar[str] = "2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87"

    def __init__(
        self, context: ADOContext, http_client: ADOHTTPClient, log: logging.Logger
    ) -> None:
        super().__init__(context, http_client, log.getChild("security"))

    def add_branch_build_policy(self, branch: str, *, build_definition_id: int) -> ADOResponse:
        """Adds a new build policy for a given branch.

        :param str branch: The git branch to set the build policy for
        :param int build_definition_id: The build definition to use when creating the build policy

        :returns: The ADO response with the data in it
        """

        request_url = f"{self.http_client.base_url(is_project=True)}/policy/Configurations?api-version=5.1-preview.1"

        body = {
            "type": {"id": ADOBranchPolicy.BUILD.value},
            "revision": 1,
            "isDeleted": False,
            "isBlocking": True,
            "isEnabled": True,
            "settings": {
                "buildDefinitionId": build_definition_id,
                "displayName": None,
                "queueOnSourceUpdateOnly": False,
                "manualQueueOnly": False,
                "validDuration": 0,
                "scope": [
                    {
                        "refName": f"refs/heads/{branch}",
                        "matchKind": "Exact",
                        "repositoryId": self._context.repository_id,
                    }
                ],
            },
        }

        response = self.http_client.post(request_url, json_data=body)
        return self.http_client.decode_response(response)

    def add_branch_required_reviewers_policy(
        self, branch: str, *, identities: List[str]
    ) -> ADOResponse:
        """Adds required reviewers when opening PRs against a given branch.

        :param str branch: The git branch to set required reviewers for
        :param List[str] identities: A list of identities to become required
                                     reviewers (should be team foundation IDs)

        :returns: The ADO response with the data in it
        """

        request_url = f"{self.http_client.base_url(is_project=True)}/policy/Configurations?api-version=5.1-preview.1"

        body = {
            "type": {"id": ADOBranchPolicy.REQUIRED_REVIEWERS.value},
            "revision": 1,
            "isDeleted": False,
            "isBlocking": True,
            "isEnabled": True,
            "settings": {
                "requiredReviewerIds": identities,
                "filenamePatterns": [],
                "addedFilesOnly": False,
                "ignoreIfSourceIsInScope": False,
                "message": None,
                "scope": [
                    {
                        "refName": f"refs/heads/{branch}",
                        "matchKind": "Exact",
                        "repositoryId": self._context.repository_id,
                    }
                ],
            },
        }

        response = self.http_client.post(request_url, json_data=body)
        return self.http_client.decode_response(response)

    def set_branch_approval_count_policy(
        self,
        branch: str,
        *,
        minimum_approver_count: int,
        creator_vote_counts: bool = False,
        reset_on_source_push: bool = False,
    ) -> ADOResponse:
        """Set minimum number of reviewers for a branch.

        :param str branch: The git branch to set minimum number of reviewers on
        :param int minimum_approver_count: The minimum number of approvals required
        :param bool creator_vote_counts: Allow users to approve their own changes
        :param bool reset_on_source_push: Reset reviewer votes when there are new changes

        :returns: The ADO response with the data in it
        """

        request_url = f"{self.http_client.base_url(is_project=True)}/policy/Configurations?api-version=5.1-preview.1"

        body = {
            "type": {"id": ADOBranchPolicy.APPROVAL_COUNT.value},
            "revision": 2,
            "isDeleted": False,
            "isBlocking": True,
            "isEnabled": True,
            "settings": {
                "minimumApproverCount": minimum_approver_count,
                "creatorVoteCounts": creator_vote_counts,
                "resetOnSourcePush": reset_on_source_push,
                "scope": [
                    {
                        "refName": f"refs/heads/{branch}",
                        "matchKind": "Exact",
                        "repositoryId": self._context.repository_id,
                    }
                ],
            },
        }

        response = self.http_client.post(request_url, json_data=body)
        return self.http_client.decode_response(response)

    def set_branch_work_item_policy(self, branch: str, *, required: bool = True) -> ADOResponse:
        """Set the work item policy for a branch.

        :param str branch: The git branch to set the work item policy on
        :param bool required: Whether or not linked work items should be mandatory

        :returns: The ADO response with the data in it
        """

        request_url = f"{self.http_client.base_url(is_project=True)}/policy/Configurations?api-version=5.1-preview.1"

        body = {
            "type": {"id": ADOBranchPolicy.WORK_ITEM.value},
            "revision": 2,
            "isDeleted": False,
            "isBlocking": required,
            "isEnabled": True,
            "settings": {
                "scope": [
                    {
                        "refName": f"refs/heads/{branch}",
                        "matchKind": "Exact",
                        "repositoryId": self._context.repository_id,
                    }
                ]
            },
        }

        response = self.http_client.post(request_url, json_data=body)
        return self.http_client.decode_response(response)

    def set_branch_permissions(
        self,
        branch: str,
        *,
        identity: TeamFoundationId,
        permissions: Dict[ADOBranchPermission, ADOBranchPermissionLevel],
    ) -> ADOResponse:
        """Set permissions for an identity on a branch.

        :param str branch: The git branch to set permissions on
        :param TeamFoundationId identity: The identity to set permissions for (should be team foundation ID)
        :param Dict[ADOBranchPermission,ADOBranchPermissionLevel] permissions: A dictionary of permissions to set

        :returns: The ADO response with the data in it
        """

        descriptor_info = self._get_descriptor_info(branch, identity)

        request_url = self.http_client.base_url(is_project=True, is_internal=True)
        request_url += "/_security/ManagePermissions?__v=5"

        updates = []
        for permission, level in permissions.items():
            updates.append(
                {
                    "PermissionId": level,
                    "PermissionBit": permission,
                    "NamespaceId": ADOSecurityClient.GIT_PERMISSIONS_NAMESPACE,
                    "Token": self._generate_updates_token(branch),
                }
            )

        package = {
            "IsRemovingIdentity": False,
            "TeamFoundationId": identity,
            "DescriptorIdentityType": descriptor_info["type"],
            "DescriptorIdentifier": descriptor_info["id"],
            "PermissionSetId": ADOSecurityClient.GIT_PERMISSIONS_NAMESPACE,
            "PermissionSetToken": self._generate_permission_set_token(branch),
            "RefreshIdentities": False,
            "Updates": updates,
            "TokenDisplayName": None,
        }

        body = {"updatePackage": json.dumps(package)}

        response = self.http_client.post(request_url, json_data=body)
        return self.http_client.decode_response(response)

    def _get_descriptor_info(self, branch: str, team_foundation_id: TeamFoundationId) -> Dict[str, str]:
        """Fetch the descriptor identity information for a given identity.

        :param str branch: The git branch of interest
        :param TeamFoundationId team_foundation_id: the unique Team Foundation GUID for the identity

        :returns: The raw descriptor info

        :raises ADOException: If we can't determine the descriptor info from the response
        """

        request_url = f"{self.http_client.base_url(is_project=True, is_internal=True)}/_security/DisplayPermissions?"

        parameters = {
            "tfid": team_foundation_id,
            "permissionSetId": ADOSecurityClient.GIT_PERMISSIONS_NAMESPACE,
            "permissionSetToken": self._generate_permission_set_token(branch),
            "__v": "5",
        }

        request_url += urllib.parse.urlencode(parameters)

        response = self.http_client.get(request_url)
        response_data = self.http_client.decode_response(response)

        try:
            descriptor_info = {
                "type": response_data["descriptorIdentityType"],
                "id": response_data["descriptorIdentifier"],
            }
        except:
            raise ADOException(
                "Could not determine descriptor info for team_foundation_id: " + str(team_foundation_id)
            )

        return descriptor_info

    def _generate_permission_set_token(self, branch: str) -> str:
        """Generate the token required for reading identity details and writing permissions.

        :param str branch: The git branch of interest

        :returns: The permission token
        """
        encoded_branch = branch.replace("/", "^")
        return f"repoV2/{self.http_client.project_id}/{self._context.repository_id}/refs^heads^{encoded_branch}/"

    def _generate_updates_token(self, branch: str) -> str:
        """Generate the token required for updating permissions.

        :param str branch: The git branch of interest

        :returns: The update token
        """

        # Encode each node in the branch to hex
        encoded_branch_nodes = [node.encode("utf-16le").hex() for node in branch.split("/")]

        encoded_branch = "/".join(encoded_branch_nodes)

        return f"repoV2/{self.http_client.project_id}/{self._context.repository_id}/refs/heads/{encoded_branch}/"
