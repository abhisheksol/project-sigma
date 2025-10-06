from rest_framework import generics, permissions
from store.operations.case_management.models import (
    CaseManagementCaseModel,
)
from store.operations.case_management.v1.generics.serializers import (
    CaseAllocationModelSerializer,
)
from store.operations.case_management.v1.utils.filters import CaseAllocationFilter
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from django_filters.rest_framework import DjangoFilterBackend
from core_utils.utils.generics.views.generic_views import CoreGenericListCreateAPIView
from rest_framework import filters
from django.db.models import Value, IntegerField

# from store.operations.case_management.v1.generics.views import get_descendant_users


class CaseallocationGenericAPIView(
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CaseManagementCaseModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["customer_name", "loan_account_number"]
    filterset_class = CaseAllocationFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            contact_score=Value(0, output_field=IntegerField()),
        )

    def get_serializer_class(self):
        return {"GET": CaseAllocationModelSerializer}.get(self.request.method)
