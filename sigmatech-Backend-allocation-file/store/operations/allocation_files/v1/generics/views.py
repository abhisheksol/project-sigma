from rest_framework import filters, generics, permissions

from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
)
from core_utils.utils.generics.views.generic_views import CoreGenericListCreateAPIView
from store.operations.allocation_files.models import AllocationFileModel

from store.operations.allocation_files.v1.upload.serializers import (
    ReUploadAllocatinFileModelSerializer,
    UploadAllocatinFileModelSerializer,
)
from store.operations.allocation_files.v1.upload.utils.common.constants import (
    ALLOCATION_FILE_API_SUCCESS_MESSAGE,
)
from store.operations.allocation_files.v1.utils.filters import AllocationFileFilter
from store.operations.allocation_files.v1.generics.serializers import (
    AllocationFileDetailModelSerializer,
    AllocationFileListSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Value, IntegerField

from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class AllocationFileGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = AllocationFileModel.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AllocationFileFilter
    search_fields = [
        "title",
        "product_assignment__process__title",
        "product_assignment__product__title",
    ]
    success_message = ALLOCATION_FILE_API_SUCCESS_MESSAGE

    def get_queryset(self):
        return self.queryset.annotate(
            cases_count=Count("CaseManagementCaseModel_allocation_file", distinct=True),
            tos_count=Value(0, output_field=IntegerField()),
            referred=Value(0, output_field=IntegerField()),
        )

    def get_serializer_class(self):
        return {
            "GET": AllocationFileListSerializer,
            "POST": UploadAllocatinFileModelSerializer,
            "PUT": ReUploadAllocatinFileModelSerializer,
        }.get(self.request.method)


class AllocationFileDetailAPIView(CoreGenericGetAPIView, generics.GenericAPIView):
    queryset = AllocationFileModel.objects.all()
    many = False
    pk_scope = "KWARGS"

    def get_serializer_class(self):
        return {"GET": AllocationFileDetailModelSerializer}.get(self.request.method)
