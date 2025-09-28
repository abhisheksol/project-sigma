from typing import List

from django.urls import path

from user_config.user_auth.api.v1.authentication import views as auth_views
from user_config.user_auth.api.v1.generics import views as generic_views

generic_urlpatterns: List = [
    path(
        "users-list-api/",
        generic_views.UserAuthUserListModelAPIView.as_view(),
        name="UserAuthUserListModelAPIView",
    )
]

authenticate_urlpatterns: List = [
    path(
        "user-login-api/",
        auth_views.UserLoginAPIView.as_view(),
        name="ObtainJSONWebTokenView",
    ),
    path(
        "user-logout-api/",
        auth_views.UserAuthUserModelLogoutAPIView.as_view(),
        name="UserAuthUserModelLogoutAPIView",
    ),
    path(
        "user-forgot-password-api/",
        auth_views.UserAuthUserModelForgotPasswordAPIView.as_view(),
        name="UserAuthUserModelForgotPasswordAPIView",
    ),
    path(
        "user-reset-password-api/",
        auth_views.UserAuthUserModelResetPasswordAPIView.as_view(),
        name="UserAuthUserModelResetPasswordAPIView",
    ),
    path(
        "user-otp-generate-api/",
        auth_views.UserManagementMobileOtpGenericAPIView.as_view(),
        name="UserManagementMobileOtpGenericAPIView",
    ),
    path(
        "user-otp-verify-api/",
        auth_views.UserManagementMobileOtpVerifyGenericAPIView.as_view(),
        name="UserManagementMobileOtpVerifyGenericAPIView",
    ),

]


urlpatterns: List = [*authenticate_urlpatterns, *generic_urlpatterns]
