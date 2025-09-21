from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView
from rest_framework import generics, permissions


from store.operations.allocation_files.v1.helper_apis.serializers import (
    AllocationFileStatusListHelperModelSerializer,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class AllocationFileStatusHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return AllocationFileStatusListHelperModelSerializer

    def get_queryset(self):
        # ✅ Return static dropdown data instead of model objects
        return AllocationFileStatusListHelperModelSerializer.get_dropdown_data()
