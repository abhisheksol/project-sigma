from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView
from rest_framework import generics, permissions


from store.operations.case_management.v1.helper_apis.serializers import (
    CaseALLocationRiskListHelperModelSerializer,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class CaseALLocationRiskHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return CaseALLocationRiskListHelperModelSerializer

    def get_queryset(self):
        # ✅ Return static dropdown data instead of model objects
        return CaseALLocationRiskListHelperModelSerializer.get_dropdown_data()
