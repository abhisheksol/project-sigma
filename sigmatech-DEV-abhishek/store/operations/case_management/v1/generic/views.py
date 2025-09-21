
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from rest_framework import generics, permissions
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from store.operations.case_management.models import CaseManagementCaseModel
from store.operations.case_management.v1.generic.serializers import CaseManagementListSerializer



class CaseManagementListGenericView(
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = CaseManagementCaseModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": CaseManagementListSerializer,  
             
        }.get(self.request.method)