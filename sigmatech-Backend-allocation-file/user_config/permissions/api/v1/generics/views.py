from rest_framework import generics, permissions
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericPostAPIView,
)
from user_config.permissions.api.v1.generics.serializers import (
    UserConfigurationLoginUserAssignedPermissionsModelSerializer,
    UserConfigurationUserAssignedPermissionsModelSerializer,
    UserConfigurationUserPermissionAssignmentSerializer,
)
from user_config.permissions.api.v1.utils.constants import (
    USER_CONFIG_PERMISSIONS_ASSIGNMENT_SUCCESS_MESSAGE,
)
from user_config.permissions.models import UserConfigPermissionsModel
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class UserConfigurationUserAssignedPermissionsAPIView(
    CoreGenericGetAPIView, CoreGenericPostAPIView, generics.GenericAPIView
):
    queryset = UserConfigPermissionsModel.objects.all().filter(
        parent_permission__isnull=True
    )
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = USER_CONFIG_PERMISSIONS_ASSIGNMENT_SUCCESS_MESSAGE

    def get_serializer_class(self):

        return {
            "GET": UserConfigurationUserAssignedPermissionsModelSerializer,
            "POST": UserConfigurationUserPermissionAssignmentSerializer,
        }.get(self.request.method)


class UserConfigurationLoginUserAssignedPermissionsAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    queryset = UserConfigPermissionsModel.objects.all().filter(
        parent_permission__isnull=True
    )
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = USER_CONFIG_PERMISSIONS_ASSIGNMENT_SUCCESS_MESSAGE

    def get_serializer_class(self):

        return {
            "GET": UserConfigurationLoginUserAssignedPermissionsModelSerializer
        }.get(self.request.method)
