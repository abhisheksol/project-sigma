from typing import List, Dict
from django.db import transaction
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from user_config.user_auth.models import UserModel
from user_config.permissions.api.v1.utils.constants import (
    INCORRECT_PAYLOAD_FORMAT_INCORRECT_ERROR,
    INCORRECT_USER_ID_ERROR_MESSAGE,
)


class UserManagementUserReAssignmentHandler(CoreGenericBaseHandler):
    """
    Handler for reassigning user reporting relationships.

    Example payload:
    {
        "assignment_data": [
            {
                "user_id": "<uuid-of-user>",
                "reports_to_id": "<uuid-of-reports-to-user>"
            }
        ]
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Stores ORM instances after validation
        self.payload_orm_instance: List[Dict[str, UserModel]] = []

    def validate_payload(self) -> bool:
        """
        Validate the payload structure.

        Returns:
            bool: True if payload is valid, False otherwise.
        """
        assignment_data = self.data.get("assignment_data")
        if not assignment_data or len(assignment_data) == 0:
            return False

        required_keys: set = {"user_id", "reports_to_id"}
        for payload in assignment_data:
            if not required_keys.issubset(payload.keys()):
                return False
        return True

    def validate(self):
        """
        Validate the payload and fetch ORM instances.
        """
        if not self.validate_payload():
            return self.set_error_message(
                error_message=INCORRECT_PAYLOAD_FORMAT_INCORRECT_ERROR
            )

        assignment_data: List[Dict] = self.data["assignment_data"]
        try:
            for data in assignment_data:
                self.payload_orm_instance.append(
                    {
                        "user": self.queryset.get(pk=data["user_id"]),
                        "reports_to": self.queryset.get(pk=data["reports_to_id"]),
                    }
                )
        except UserModel.DoesNotExist:
            return self.set_error_message(error_message=INCORRECT_USER_ID_ERROR_MESSAGE)

    def create(self):
        """
        Perform the reassignment of users inside an atomic transaction.
        """
        with transaction.atomic():
            for data in self.payload_orm_instance:
                user_instance: UserModel = data["user"]
                reports_to_instance: UserModel = data["reports_to"]

                user_instance.reports_to = reports_to_instance
                user_instance.save(update_fields=["reports_to"])
