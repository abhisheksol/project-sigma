from django.urls import path

from user_config.permissions.api.v1.generics import views

urlpatterns: list = [
    path(
        "user-assigned-permissions-list-api/",
        views.UserConfigurationUserAssignedPermissionsAPIView.as_view(),
        name="UserConfigurationUserAssignedPermissionsAPIView",
    ),
    path(
        "login-user-assigned-permissions-list-api/",
        views.UserConfigurationLoginUserAssignedPermissionsAPIView.as_view(),
        name="UserConfigurationLoginUserAssignedPermissionsAPIView",
    ),
]
