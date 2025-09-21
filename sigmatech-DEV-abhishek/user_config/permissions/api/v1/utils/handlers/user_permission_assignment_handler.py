from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from typing import List, Dict, Union
from django.db.models.query import QuerySet
from user_config.permissions.api.v1.utils.constants import (
    INCORRECT_PAYLOAD_FORMAT_INCORRECT_ERROR,
    INCORRECT_USER_ID_ERROR_MESSAGE,
    PERMISSION_ID_INCORRECT_ERROR_MESSAGE,
)
from user_config.permissions.models import (
    UserConfigPermissionsModel,
    UserConfigUserAssignedPermissionsModel,
)
from user_config.user_auth.models import UserModel
from django.db import transaction
from user_config.accounts.api.v1.utils.constants import FIELD_REQUIRED_ERROR_MESSAGE


class UserConfigurationUserPermissionAssignmentHandler(CoreGenericBaseHandler):
    """
    Handler for assigning or revoking user permissions.

    Payload format:
        {
            "user_id": "<uuid>",
            "permissions": [
                {
                    "id": "<permission_id>",
                    "read_only_access": true/false,
                    "all_access": true/false
                }
            ]
        }
    """

    permissions: List[Dict[str, Union[str, bool]]]
    user_instance: UserModel
    _activity_type: str = "USER_PERMISSION_ASSIGNMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def is_payload_format_valid(self) -> bool:
        """
        Validate the incoming permissions payload.
        Ensures that each permission dictionary contains valid keys.
        """
        allowed_keys: set = {"id", "read_only_access", "all_access"}

        for permission in self.permissions:
            # Must contain at least id
            if "id" not in permission:
                return False

            if not permission["id"]:
                return False

            # Ensure only allowed keys are present
            if not set(permission.keys()).issubset(allowed_keys):
                return False

            # Ensure boolean fields are valid
            for key in ("read_only_access", "all_access"):
                if key in permission and not isinstance(permission[key], bool):
                    return False

        return True

    def validate(self):
        """Validate the request data."""
        if not self.data.get("user_id"):
            return self.set_error_message(
                error_message=f"user_id {FIELD_REQUIRED_ERROR_MESSAGE}", key="user_id"
            )

        try:
            self.user_instance: UserModel = UserModel.objects.get(
                pk=self.data["user_id"]
            )
        except UserModel.DoesNotExist:
            return self.set_error_message(
                error_message=INCORRECT_USER_ID_ERROR_MESSAGE,
                key="user_id",
            )

        self.permissions: List[Dict[str, Union[str, bool]]] = self.data["permissions"]

        if not self.is_payload_format_valid():
            return self.set_error_message(
                error_message=INCORRECT_PAYLOAD_FORMAT_INCORRECT_ERROR,
                key="permissions",
            )

        # Validate permission IDs exist in DB
        permissions_id_list: List[str] = [i["id"] for i in self.permissions]

        self.queryset: QuerySet[UserConfigPermissionsModel] = self.queryset.filter(
            pk__in=permissions_id_list, parent_permission__isnull=False
        )

        if self.queryset.count() != len(permissions_id_list):
            return self.set_error_message(
                error_message=PERMISSION_ID_INCORRECT_ERROR_MESSAGE,
                key="permissions",
            )

        self.logger.debug(
            f"Validation complete. User={self.data['user_id']}, "
            f"Permissions={permissions_id_list}"
        )

    def create(self):
        """
        Assign/update user permissions:
          - If read_only_access or all_access is True → assign/update
          - If both are False → revoke
        """
        with transaction.atomic():
            user_assigned_queryset: QuerySet[UserConfigUserAssignedPermissionsModel] = (
                UserConfigUserAssignedPermissionsModel.objects.filter(
                    user=self.user_instance
                )
            )

            for permission in self.queryset:
                incoming_permission = next(
                    (p for p in self.permissions if p["id"] == str(permission.id)), None
                )
                if not incoming_permission:
                    continue

                read_only_access = incoming_permission.get("read_only_access", False)
                all_access = incoming_permission.get("all_access", False)

                # If both are False → revoke (remove assignment)
                if not read_only_access and not all_access:
                    deleted_count, _ = user_assigned_queryset.filter(
                        permission=permission
                    ).delete()
                    if deleted_count > 0:
                        self.logger.info(
                            f"Revoked permission '{permission.title}' "
                            f"from user '{self.user_instance.username}'"
                        )
                    continue

                # Otherwise → grant or update assignment
                obj, created = (
                    UserConfigUserAssignedPermissionsModel.objects.update_or_create(
                        user=self.user_instance,
                        permission=permission,
                        defaults={
                            "read_only_access": read_only_access,
                            "all_access": all_access,
                            "core_generic_created_by": self.request.user.UserDetailModel_user,
                        },
                    )
                )

                if created:
                    self.logger.info(
                        f"Granted permission '{permission.title}' "
                        f"to user '{self.user_instance.username}'"
                    )
                else:
                    self.logger.info(
                        f"Updated permission '{permission.title}' flags "
                        f"for user '{self.user_instance.username}'"
                    )
            # TODO update Base Handler and set toast message
            self.set_toast_message_value(value=self.user_instance.username)
            self.update_core_generic_updated_by(instance=self.user_instance)
            self.logger.info(
                f"Permissions updated successfully for user '{self.user_instance.username}'"
            )
