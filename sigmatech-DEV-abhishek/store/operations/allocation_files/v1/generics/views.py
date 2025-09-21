from rest_framework import filters
from rest_framework import generics, permissions

from store.operations.allocation_files.models import AllocationFileModel

from store.operations.allocation_files.v1.utils.filters import AllocationFileFilter
from store.operations.allocation_files.v1.generics.serializers import (
    AllocationFileListSerializer,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from django_filters.rest_framework import DjangoFilterBackend


# class AllocatinFileGenericAPIView(CoreGenericPostAPIView, generics.ListCreateAPIView):
#     queryset = UserModel.objects.all()
#     authentication_classes = [CustomAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get_serializer_class(self):

#         return {"POST": None}.get(self.request.method)


class AllocationFileGenericAPIView(
    # CoreGenericPutAPIView,
    # CoreGenericDeleteAPIView,
    # CoreGenericListCreateAPIView,
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

    def get_serializer_class(self):
        return {
            "GET": AllocationFileListSerializer,
        }.get(self.request.method)
