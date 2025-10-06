from rest_framework import serializers

from user_config.permissions.api.v1.utils.handlers.user_permission_assignment_handler import (
    UserConfigurationUserPermissionAssignmentHandler,
)
from user_config.permissions.api.v1.utils.permissions_utils import (
    get_permissions_and_user_access,
)
from user_config.permissions.models import UserConfigPermissionsModel
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from user_config.user_auth.models import UserModel


class UserConfigurationUserAssignedPermissionsModelSerializer(
    serializers.ModelSerializer
):
    sub_permissions = serializers.SerializerMethodField()

    class Meta:
        model = UserConfigPermissionsModel
        fields = ["id", "title", "sub_permissions", "description", "icons"]

    def get_sub_permissions(self, obj: UserConfigPermissionsModel):
        return get_permissions_and_user_access(
            permission_instance=obj,
            user_instance=UserModel.objects.get(
                pk=self.context["request"].GET.dict().get("user_id")
            ),
            is_login_user=False,
        )


class UserConfigurationLoginUserAssignedPermissionsModelSerializer(
    serializers.ModelSerializer
):
    sub_permissions = serializers.SerializerMethodField()

    class Meta:
        model = UserConfigPermissionsModel
        fields = ["id", "title", "sub_permissions"]

    def get_sub_permissions(self, obj: UserConfigPermissionsModel):
        return get_permissions_and_user_access(
            permission_instance=obj,
            user_instance=self.context["request"].user,
            is_login_user=True,
        )


class UserConfigurationUserPermissionAssignmentDetailSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    read_only_access = serializers.BooleanField()
    all_access = serializers.BooleanField()


class UserConfigurationUserPermissionAssignmentSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):

    queryset = UserConfigPermissionsModel.objects.all()
    user_id = serializers.CharField()
    permissions = UserConfigurationUserPermissionAssignmentDetailSerializer(
        many=True, required=True
    )
    handler_class = UserConfigurationUserPermissionAssignmentHandler
