import logging
from typing import Dict

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from core.settings import logger
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from user_config.user_auth.api.v1.utils.authentication.jwt_response_payload_handler_utils import (
    jwt_response_payload_handler,
)
from user_config.user_auth.api.v1.utils.authentication.user_login_utils import (
    ValidateUserLogin,
)
from user_config.user_auth.api.v1.utils.handler.forgot_password_handler import (
    UserAuthUserForgotPasswordHandler,
    UserAuthUserResetPasswordHandler,
)
from user_config.user_auth.api.v1.utils.handler.logout_handler import (
    UserAuthUserModelLogoutHandler,
)
from user_config.user_auth.models import BlackListTokenModel, MobileOTPModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _gettext
from user_config.user_auth.api.v1.utils.handler.otp_genrate_handler import (
    OtpGenerateHandler,
)
from user_config.user_auth.api.v1.utils.handler.otpverifyhandler import OtpverifyHandler


# Logger setup with application context
logger: logging.LoggerAdapter = logging.LoggerAdapter(
    logger, {"app_name": "user_config.user_auth.api.v1.authentication.serializers.py"}
)


class UserLoginWebTokenSerializer(JSONWebTokenSerializer):
    """
    Serializer for handling user login authentication with JWT tokens.
    It validates user credentials, ensures proper authentication, and
    returns a JWT token upon successful login.
    """

    # Logger specific to this serializer
    logger: logging.LoggerAdapter = logging.LoggerAdapter(
        logger, {"app_name": "UserLoginWebTokenSerializer"}
    )

    # Fields required for user authentication
    login_id: str = serializers.CharField(
        required=True, help_text="User login_id address."
    )
    password: str = serializers.CharField(
        required=True, write_only=True, help_text="User password."
    )
    re_login: bool = serializers.BooleanField(
        default=True, help_text="Flag to allow re-login if multi-login is disabled."
    )

    def validate(self, data: Dict) -> Dict:
        """
        Validate user login credentials and generate a JWT token if successful.

        Args:
            data (dict): A dictionary containing user-provided email, password, and re-login flag.

        Returns:
            dict: A dictionary containing the authenticated user instance and JWT token.

        Raises:
            serializers.ValidationError: If authentication fails due to incorrect credentials
                                         or multiple active logins (if restricted).
        """
        try:
            # ? Initialize user login validation utility
            validate_user_login: ValidateUserLogin = ValidateUserLogin(
                login_id=data["login_id"],
                password=data["password"],
                re_login=data["re_login"],
            )

            # ? Validate user credentials and check for errors
            validation_errors: str = validate_user_login.validate_login()
            # ? Raise an error if validation fails
            if validation_errors:
                raise serializers.ValidationError(validation_errors)

            # ? Generate JWT token after successful validation
            jwt_token: str = validate_user_login.set_jwt_token()

            process_user: Dict = jwt_response_payload_handler(
                request=self.context["request"],
                user=validate_user_login.user_instance,
                token=jwt_token,
            )

            # ? Return authenticated user and token
            return process_user
        except Exception as e:
            self.logger.error(f"Login failed, {str(e)}")
            raise serializers.ValidationError(
                _gettext("Login failed, Invalid email or password. Please try again.")
            )


class UserAuthUserModelLogoutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = UserAuthUserModelLogoutHandler
    queryset = BlackListTokenModel.objects.all()


class UserAuthUserModelForgotPasswordSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = UserAuthUserForgotPasswordHandler
    queryset = get_user_model().objects.all()
    login_id = serializers.CharField()


class UserAuthUserModelResetPasswordSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = UserAuthUserResetPasswordHandler
    queryset = get_user_model().objects.all()
    token = serializers.CharField()
    password = serializers.CharField()


# mobile otp reset


class UserManagementUserCreateOtpModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = OtpGenerateHandler
    # mobile_otp = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    # is_expired = serializers.BooleanField(required=False, default=False)
    otp = serializers.CharField(required=True)

    class Meta:
        model = MobileOTPModel
        fields = [
            "otp",
            "phone_number",
            # "is_expired"
        ]


class UserManagementUserVerifyOtpModelSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = OtpverifyHandler
    phone_number = serializers.CharField(required=True)
    mobile_otp = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    class Meta:
        model = MobileOTPModel
        fields = ["phone_number", "token", "mobile_otp"]
