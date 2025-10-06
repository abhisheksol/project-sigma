from typing import Dict, Optional, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction

from core_utils.utils.format_validator import (
    is_format_validator_email,
    is_valid_password,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core_utils.utils.jwt_token_utils import decode_jwt, encode_jwt
from user_config.user_auth.api.v1.utils.constants import (
    FAILED_TO_RESET_PASSWORD_ERROR_MESSAGE,
    INCORRECT_CREDENTIALS_ERROR_MESSAGE,
    INCORRECT_EMAIL_FORMAT_ERROR_MESSAGE,
    INVALID_PASSWORD_LINK_OR_EXPIRED_ERROR_MESSAGE,
    PASSWORD_REQUIRED_ERROR_MESSAGE,
    PASSWORD_VALIDATION_ERROR_MESSAGE,
)
from user_config.user_auth.models import BlackListTokenModel
from user_config.user_auth.utils.email_templates.forgot_password_email_templates import (
    forgot_password_send_email,
)


class UserAuthUserForgotPasswordHandler(CoreGenericBaseHandler):
    """
    Handles the forgot password process.

    Responsibilities:
    - Validates user's login ID (email/username).
    - Checks account existence and status.
    - Generates JWT token and stores it in `BlackListTokenModel`.
    - Sends password reset email to user.
    """

    user_instance: AbstractBaseUser

    def validate(self) -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
        """
        Validates the login_id provided by the user.

        Returns:
            Optional[Dict]: Error message dictionary if validation fails, otherwise None.
        """
        self.context["logger"].info("Validating forgot password request.")

        # Validate email format if login_id is email
        if "@" in self.data["login_id"] and not is_format_validator_email(
            email=self.data["login_id"]
        ):
            self.context["logger"].warning(
                f"Invalid email format. {self.data['login_id']}"
            )
            return self.set_error_message(INCORRECT_EMAIL_FORMAT_ERROR_MESSAGE)

        is_email_login: bool = is_format_validator_email(email=self.data["login_id"])
        login_id_filter: Dict[str, str] = {}

        if is_email_login:
            login_id_filter["email__iexact"] = self.data["login_id"]
        else:
            login_id_filter["login_id__iexact"] = self.data["login_id"]
        # Check if user exists and is active
        if not self.queryset.filter(**login_id_filter, is_active=True).exists():
            self.context["logger"].warning(
                "No active account found for given login_id."
            )
            return self.set_error_message(INCORRECT_CREDENTIALS_ERROR_MESSAGE)

        self.user_instance = self.queryset.get(**login_id_filter, is_active=True)
        self.context["logger"].info(
            f"User {self.user_instance.email} validated for forgot password flow."
        )
        return None

    def create(self) -> None:
        """
        Creates and stores a reset token, then sends the password reset email.

        Raises:
            Exception: If any error occurs during token creation or email sending.
        """
        try:
            with transaction.atomic():
                token: str = encode_jwt(user_id=str(self.user_instance.pk))

                token_instance: BlackListTokenModel = (
                    BlackListTokenModel.objects.create(
                        token=token,
                        user=self.user_instance,
                        is_login=True,
                    )
                )
                self.context["logger"].info(
                    f"Token {token_instance.pk} generated for user {self.user_instance.pk}."
                )

                forgot_password_send_email(
                    user_instance=self.user_instance, token=token
                )
                self.context["logger"].info(
                    f"Password reset email sent to {self.user_instance.email}."
                )

        except Exception as e:
            self.context["logger"].error(f"Unable to send reset email: {str(e)}")
            raise Exception("Unable to send reset mail")


class UserAuthUserResetPasswordHandler(CoreGenericBaseHandler):
    """
    Handles password reset process.

    Responsibilities:
    - Validates reset token and password.
    - Updates user password.
    - Invalidates the used reset token.
    """

    def validate(self) -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
        """
        Validates the reset password request by verifying token and password constraints.

        Returns:
            Optional[Dict]: Error message dictionary if validation fails, otherwise None.
        """
        self.context["logger"].info("Validating reset password token.")

        if not self.data.get("password"):
            self.context["logger"].warning(PASSWORD_REQUIRED_ERROR_MESSAGE)
            return self.set_error_message(error_message=PASSWORD_REQUIRED_ERROR_MESSAGE)
        if not is_valid_password(password=self.data["password"]):
            self.context["logger"].warning(
                f'Password : {self.data["password"]} {PASSWORD_VALIDATION_ERROR_MESSAGE}'
            )
            return self.set_error_message(
                error_message=PASSWORD_VALIDATION_ERROR_MESSAGE
            )
        if not BlackListTokenModel.objects.filter(token=self.data["token"]).exists():
            self.context["logger"].warning("Token not found in database.")
            return self.set_error_message(
                error_message=FAILED_TO_RESET_PASSWORD_ERROR_MESSAGE
            )

        if not BlackListTokenModel.objects.filter(
            token__iexact=self.data["token"], is_login=True
        ).exists():
            self.context["logger"].warning("Token expired or already used.")
            return self.set_error_message(
                error_message=INVALID_PASSWORD_LINK_OR_EXPIRED_ERROR_MESSAGE
            )

        token_details: Dict = decode_jwt(token=self.data["token"])

        if "is_error" in token_details and token_details["is_error"]:
            self.context["logger"].warning(
                f"Token decode error: {token_details['description']}"
            )
            return self.set_error_message(token_details["description"])

        if (
            not get_user_model()
            .objects.filter(pk=token_details["user_id"], is_active=True)
            .exists()
        ):
            self.context["logger"].warning("No active user associated with token.")
            self.data["error_message"] = INCORRECT_CREDENTIALS_ERROR_MESSAGE

        self.data["user_id"] = token_details["user_id"]
        self.context["logger"].info(
            f"Password reset validated for user {self.data['user_id']}."
        )

    def create(self) -> None:
        """
        Resets the user's password and marks the token as used.

        Raises:
            Exception: If any error occurs while saving the new password or updating the token.
        """
        try:
            with transaction.atomic():
                user_instance: AbstractBaseUser = get_user_model().objects.get(
                    pk=self.data["user_id"]
                )

                user_instance.set_password(self.data["password"])
                user_instance.save()
                self.context["logger"].info(
                    f"Password updated successfully for user {user_instance.pk}."
                )

                BlackListTokenModel.objects.filter(
                    token=self.data["token"], is_delete=False, is_login=True
                ).update(is_delete=True, is_login=False)
                self.context["logger"].info(
                    f"Token {self.data['token']} marked as used."
                )

        except Exception as e:
            self.context["logger"].error(f"Error while resetting password: {str(e)}")
            raise Exception(f"Error while resetting password: {str(e)}")
