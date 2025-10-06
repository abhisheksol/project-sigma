from django.db import transaction
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from user_config.user_auth.api.v1.utils.constants import (
    USER_LOGOUT_INCORRECT_USER_ERROR_MESSAGE,
)
from user_config.user_auth.models import BlackListTokenModel
from user_config.user_auth.utils.custom_authentication.validations import (
    ExtractAuthenticationDetails,
)


class UserAuthUserModelLogoutHandler(CoreGenericBaseHandler):
    """
    Handles the logout process for a user in the authentication system.

    This class extends `CoreGenericBaseHandler` and provides `validate`
    and `create` methods to process user logout. It ensures the token is valid
    and active before logging the user out by marking the token as inactive and deleted.
    """

    _activity_type: str = "LOGOUT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        """
        Validates whether the provided JWT token is associated with a logged-in,
        non-deleted user.

        - Extracts and decodes the JWT token from the request headers.
        - Checks if a token entry exists for the current user in a valid state.
        - Adds the token to `self.data` if valid, or sets an error message if invalid.
        """
        # Extract and decode the JWT token
        user_auth_headers: ExtractAuthenticationDetails = ExtractAuthenticationDetails(
            self.request
        )
        user_token: str = (
            user_auth_headers.jwt_token.decode("utf-8")
            if isinstance(user_auth_headers.jwt_token, bytes)
            else user_auth_headers.jwt_token
        )

        # Check if the token exists for the logged-in, non-deleted user
        if not self.queryset.filter(
            token=user_token,
            user=self.request.user,
            is_login=True,
            is_delete=False,
        ).exists():
            # Set error message if token is not found or invalid
            self.data["error_message"] = USER_LOGOUT_INCORRECT_USER_ERROR_MESSAGE

        # Save token for use in the create method
        self.data["token"] = user_token

    def create(self):
        """
        Performs the logout operation by marking the token as logged out and deleted.

        - Uses a transaction to ensure atomicity.
        - Updates `is_login` and `is_delete` fields for the token in the database.
        - Removes the token from `self.data` after a successful update.
        """
        try:
            with transaction.atomic():
                # Update token status to reflect logout
                self.queryset.filter(
                    token=self.data["token"],
                    user=self.request.user,
                    is_login=True,
                    is_delete=False,
                ).update(
                    is_login=False,
                    is_delete=True,
                )
                instance: BlackListTokenModel = self.queryset.filter(
                    token=self.data["token"],
                ).last()
                # Remove token from response data
                self.data.pop("token")
                self.set_toast_message_value(value=self.request.user.username)
                if instance:
                    # ? if the instance exists update activity log
                    self.update_core_generic_created_by(instance=instance)

        except Exception as e:
            # Raise exception if the logout operation fails
            raise Exception(f"Error while logging out user : {str(e)}")
