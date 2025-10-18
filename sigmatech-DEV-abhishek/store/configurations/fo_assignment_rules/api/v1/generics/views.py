from rest_framework import generics, permissions
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from store.configurations.fo_assignment_rules.api.v1.generics.serializers import (
    ConfigurationFOAssignmentRulesPutSerializer,
    ConfigurationFOAssignmentRulesSerializer,
    FOAssignmentRulesResetSerializer,
)
from store.configurations.fo_assignment_rules.models import (
    ConfigurationFOAssignmentRuleGroupModel,
    ConfigurationFOAssignmentRulesModel,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class ConfigurationFOAssignmentRulesAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = ConfigurationFOAssignmentRulesModel
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False

    def get_object(self):
        return ConfigurationFOAssignmentRulesModel.objects.get()

    def get_serializer_class(self):
        return {
            "GET": ConfigurationFOAssignmentRulesSerializer,
            "PUT": ConfigurationFOAssignmentRulesPutSerializer,
        }.get(self.request.method)


class ConfigurationFOAssignmentRuleResetAPIView(
    CoreGenericGetAPIView, CoreGenericPutAPIView, generics.GenericAPIView
):
    queryset = ConfigurationFOAssignmentRuleGroupModel
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False

    def get_object(self):
        return ConfigurationFOAssignmentRuleGroupModel.objects.get()

    def get_serializer_class(self):
        return {
            "PUT": FOAssignmentRulesResetSerializer,
        }.get(self.request.method)
