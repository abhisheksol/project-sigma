from user_config.user_auth.models import BlackListTokenModel, MobileOTPModel
from rest_framework import generics, permissions, views, status
from core_utils.utils.generics.views.generic_views import (
    CoreGenericListCreateAPIView,
    CoreGenericPostAPIView,
    CoreGenericPutAPIView,
)
from .serializers import (
    UserAuthUserModelForgotPasswordSerializer,
    UserAuthUserModelLogoutSerializer,
    UserAuthUserModelResetPasswordSerializer,
    UserLoginWebTokenSerializer,
    UserManagementUserCreateOtpModelSerializer,
    UserManagementUserVerifyOtpModelSerializer,
)
from user_config.user_auth.api.v1.utils.constants import (
    FORGOT_RESET_PASSWORD_SUCCESS_MESSAGE,
    LOGIN_FAILED_INVALID_ERROR_MESSAGE,
    USER_LOGOUT_SUCCESS_MESSAGE,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import logging
from core.settings import logger


class UserAuthUserModelLogoutAPIView(
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    queryset = BlackListTokenModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = USER_LOGOUT_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {
            "POST": UserAuthUserModelLogoutSerializer,
        }

        return serializer_class.get(self.request.method)


class UserAuthUserModelForgotPasswordAPIView(
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    queryset = get_user_model().objects.all()
    success_message = FORGOT_RESET_PASSWORD_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {
            "POST": UserAuthUserModelForgotPasswordSerializer,
        }
        return serializer_class.get(self.request.method)


class UserAuthUserModelResetPasswordAPIView(
    CoreGenericPutAPIView,
    generics.GenericAPIView,
):
    queryset = get_user_model().objects.all()
    success_message = FORGOT_RESET_PASSWORD_SUCCESS_MESSAGE

    def get_serializer_class(self):
        serializer_class = {
            "PUT": UserAuthUserModelResetPasswordSerializer,
        }
        return serializer_class.get(self.request.method)


class UserLoginAPIView(views.APIView):
    """
    Custom API view for user login that uses UserLoginWebTokenSerializer
    to validate credentials and return JWT token.
    """

    logger = logging.LoggerAdapter(logger, {"app_name": "UserLoginView"})

    def post(self, request, *args, **kwargs):
        serializer: UserLoginWebTokenSerializer = UserLoginWebTokenSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        self.logger.error(f"User login failed: {serializer.errors}")

        return Response(
            {
                "message": LOGIN_FAILED_INVALID_ERROR_MESSAGE,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Mobile otp reset and verify


class UserManagementMobileOtpGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPostAPIView,
    generics.ListCreateAPIView,
):
    queryset = MobileOTPModel.objects.all()

    def get_serializer_class(self):

        return {
            "POST": UserManagementUserCreateOtpModelSerializer,
            # "PUT": UserManagementUserUpdateModelSerializer,
        }.get(self.request.method)


class UserManagementMobileOtpVerifyGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPostAPIView,
    generics.ListCreateAPIView,
):
    queryset = MobileOTPModel.objects.all()

    def get_serializer_class(self):

        return {
            "POST": UserManagementUserVerifyOtpModelSerializer,
            # "PUT": UserManagementUserUpdateModelSerializer,
        }.get(self.request.method)
