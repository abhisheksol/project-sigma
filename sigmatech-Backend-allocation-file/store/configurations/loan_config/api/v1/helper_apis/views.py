from rest_framework import generics, permissions
from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from .serializers import (
    LoanConfigurationsBuckeRangeHelperModelSerializer,
    LoanConfigurationsBucketHelperModelSerializer,
    LoanConfigurationsMonthlyCycleHelperModelSerializer,
    LoanConfigurationsProcessHelperModelSerializer,
    LoanConfigurationsProductHelperModelSerializer,
)


# --------------------------------Process Helper API View--------------------------------


class LoanConfigurationsProcessHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProcessModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by("title")

    def get_serializer_class(self):

        return {
            "GET": LoanConfigurationsProcessHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------Product Helper API View--------------------------------


class LoanConfigurationsProductHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsProductsModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        process_ids = self.request.query_params.get("process_id")
        qs = self.queryset.order_by("title")

        if process_ids:
            # split into list
            process_ids_list = [
                pid.strip() for pid in process_ids.split(",") if pid.strip()
            ]

            # get all product_ids linked to any of these processes
            product_ids = LoanConfigurationsProductAssignmentModel.objects.filter(
                process_id__in=process_ids_list
            ).values_list("product_id", flat=True)

            qs = qs.filter(id__in=product_ids)

        return qs

    def get_serializer_class(self):
        return {
            "GET": LoanConfigurationsProductHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------MonthlyCycle Helper API View--------------------------------


class LoanConfigurationsMonthlyCycleHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsMonthlyCycleModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by("title")

    def get_serializer_class(self):

        return {
            "GET": LoanConfigurationsMonthlyCycleHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------Bucket Helper API View--------------------------------


class LoanConfigurationsBucketHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = LoanConfigurationsBucketModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by("title")

    def get_serializer_class(self):

        return {
            "GET": LoanConfigurationsBucketHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------Bucket Range Helper API View--------------------------------


class LoanConfigurationsBucketRangeHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = BucketRangeModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by("core_generic_created_at")

    def get_serializer_class(self):

        return {
            "GET": LoanConfigurationsBuckeRangeHelperModelSerializer,
        }.get(self.request.method)
