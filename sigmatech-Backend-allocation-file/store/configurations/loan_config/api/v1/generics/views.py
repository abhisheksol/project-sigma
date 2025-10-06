from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from store.configurations.loan_config.api.v1.filters.filters import (
    BucketFilterSet,
    MonthlyCycleFilterSet,
    ProductAssignmentFilterSet,
    ProductFilterSet,
)
from store.configurations.loan_config.api.v1.utils.constants import (
    BUCKET_SUCCESS_MESSAGE,
    MONTHLYCYCLE_SUCCESS_MESSAGE,
    PROCESS_SUCCESS_MESSAGE,
    PRODUCT_SUCCESS_MESSAGE,
)
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)

from store.configurations.loan_config.api.v1.generics.serializers import (
    LoanConfigurationsBucketCreateModelSerializer,
    LoanConfigurationsBucketListModelSerializer,
    LoanConfigurationsBucketPutSerializer,
    LoanConfigurationsBucketRangeListModelSerializer,
    LoanConfigurationsMonthlyCycleCreateModelSerializer,
    LoanConfigurationsMonthlyCycleListModelSerializer,
    LoanConfigurationsMonthlyCyclePutSerializer,
    LoanConfigurationsProcessCreateModelSerializer,
    LoanConfigurationsProcessListModelSerializer,
    LoanConfigurationsProcessPutSerializer,
    LoanConfigurationsProcessDetailModelSerializer,
    LoanConfigurationsProductAssignmentCreateModelSerializer,
    LoanConfigurationsProductAssignmentListModelSerializer,
    LoanConfigurationsProductAssignmentPutSerializer,
    LoanConfigurationsProductCreateModelSerializer,
    LoanConfigurationsProductListModelSerializer,
    LoanConfigurationsProductPutSerializer,
)


from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class LoanConfigurationsProcessGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProcessModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title"]
    success_message = PROCESS_SUCCESS_MESSAGE
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsProcessListModelSerializer,
            "POST": LoanConfigurationsProcessCreateModelSerializer,
            "PUT": LoanConfigurationsProcessPutSerializer,
        }.get(self.request.method)


# -------------------------------------Product Model View-------------------------------------


class LoanConfigurationsProductGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProductsModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "title",
    ]
    filterset_class = ProductFilterSet
    success_message = PRODUCT_SUCCESS_MESSAGE
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsProductListModelSerializer,
            "POST": LoanConfigurationsProductCreateModelSerializer,
            "PUT": LoanConfigurationsProductPutSerializer,
        }.get(self.request.method)


# -------------------------------------Monthly Cycle View-------------------------------------


class LoanConfigurationsMonthlyCycleGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsMonthlyCycleModel.objects.all()
    success_message = MONTHLYCYCLE_SUCCESS_MESSAGE
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title"]
    filterset_class = MonthlyCycleFilterSet
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsMonthlyCycleListModelSerializer,
            "POST": LoanConfigurationsMonthlyCycleCreateModelSerializer,
            "PUT": LoanConfigurationsMonthlyCyclePutSerializer,
        }.get(self.request.method)


# -------------------------------------Bucket View-----------------------------------------------


class LoanConfigurationsBucketGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsBucketModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title"]
    filterset_class = BucketFilterSet
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = BUCKET_SUCCESS_MESSAGE

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsBucketListModelSerializer,
            "POST": LoanConfigurationsBucketCreateModelSerializer,
            "PUT": LoanConfigurationsBucketPutSerializer,
        }.get(self.request.method)


# -------------------------------------Bucket Range View-----------------------------------------------


class LoanConfigurationsBucketRangeGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = BucketRangeModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsBucketRangeListModelSerializer,
        }.get(self.request.method)


# -------------------------------------Product Assignment View-----------------------------------------------


class LoanConfigurationsProductAssignmentGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProductAssignmentModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductAssignmentFilterSet
    search_fields = ["product__title"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsProductAssignmentListModelSerializer,
            "POST": LoanConfigurationsProductAssignmentCreateModelSerializer,
            "PUT": LoanConfigurationsProductAssignmentPutSerializer,
        }.get(self.request.method)


class LoanConfigurationsProductDetailGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProcessModel.objects.all()
    success_message = PROCESS_SUCCESS_MESSAGE
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False
    pk_scope = "KWARGS"

    def get_serializer_class(self):

        return {
            "GET": LoanConfigurationsProcessDetailModelSerializer,
        }.get(self.request.method)
