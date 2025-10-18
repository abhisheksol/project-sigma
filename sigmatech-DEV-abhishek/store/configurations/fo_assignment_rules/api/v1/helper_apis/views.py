from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView


from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from rest_framework import generics, permissions

from store.configurations.fo_assignment_rules.api.v1.helper_apis.serializers import (
    FOAssignementUSerHelperModelSerializer,
    FOAssignementZoneHelperModelSerializer,
)
from store.configurations.region_config.models import RegionConfigurationPincodeModel
from user_config.user_auth.models import UserModel
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from user_config.user_auth.enums import UserRoleEnum


# user helper apis


class FOAssignementUserHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            user_role__role=UserRoleEnum.FIELD_OFFICER.value,
            **STATUS_ACTIVATED_GLOBAL_FILTERSET
        )

    def get_serializer_class(self):
        return {
            "GET": FOAssignementUSerHelperModelSerializer,
        }.get(self.request.method)


class FOAssignementZoneHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = RegionConfigurationPincodeModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": FOAssignementZoneHelperModelSerializer,
        }.get(self.request.method)
