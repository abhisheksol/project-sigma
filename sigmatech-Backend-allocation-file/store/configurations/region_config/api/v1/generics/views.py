from core_utils.utils.generics.views.generic_views import (
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from store.configurations.region_config.api.v1.filters.filters import (
    RegionConfigurationAreaFilter,
    RegionConfigurationCityFilter,
    RegionConfigurationPincodeFilter,
)
from store.configurations.region_config.api.v1.generics.serializers import (
    RegionConfigurationAreaCreateModelSerializer,
    RegionConfigurationAreaListModelSerializer,
    RegionConfigurationAreaPutSerializer,
    RegionConfigurationCityCreateModelSerializer,
    RegionConfigurationCityListModelSerializer,
    RegionConfigurationCityPutSerializer,
    RegionConfigurationPincodeCreateModelSerializer,
    RegionConfigurationPincodeListModelSerializer,
    RegionConfigurationPincodePutSerializer,
    RegionConfigurationRegionCreateModelSerializer,
    RegionConfigurationRegionListModelSerializer,
    RegionConfigurationRegionPutSerializer,
    RegionConfigurationZoneCreateModelSerializer,
    RegionConfigurationZoneListModelSerializer,
    RegionConfigurationZonePutSerializer,
)
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    AREA_SUCCESS_MESSAGE,
    CITY_SUCCESS_MESSAGE,
    PINCODE_SUCCESS_MESSAGE,
    REGION_SUCCESS_MESSAGE,
    ZONE_SUCCESS_MESSAGE,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count

# ----------------------------------- Region Configuration View ----------------------------------


class RegionConfigurationRegionGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    # Explicitly define queryset at class level
    queryset = RegionConfigurationRegionModel.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title"]
    ordering_fields = [
        "title",
        "status",
        "number_of_zones",
        "number_of_cities",
        "number_of_pincodes",
    ]
    ordering = ["-core_generic_created_at"]  # default ordering
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = REGION_SUCCESS_MESSAGE

    def get_queryset(self):
        qs = RegionConfigurationRegionModel.objects.with_counts()

        for region in qs:
            print(
                f"Region: {region.title}, "
                f"Zones: {region.number_of_zones}, "
                f"Cities: {region.number_of_cities}, "
                f"Pincodes: {region.number_of_pincodes}"
            )

        return RegionConfigurationRegionModel.objects.with_counts()

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationRegionListModelSerializer,
            "POST": RegionConfigurationRegionCreateModelSerializer,
            "PUT": RegionConfigurationRegionPutSerializer,
        }.get(self.request.method)


# ----------------------------------- Region Configuration Zone View ----------------------------------


# RegionConfigurationZoneModel
class RegionConfigurationZoneGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = RegionConfigurationZoneModel.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering = ["-core_generic_created_at"]
    search_fields = ["title"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = ZONE_SUCCESS_MESSAGE

    def get_queryset(self):
        return RegionConfigurationZoneModel.objects.with_details()

    def get_serializer_class(self):

        return {
            "GET": RegionConfigurationZoneListModelSerializer,
            "POST": RegionConfigurationZoneCreateModelSerializer,
            "PUT": RegionConfigurationZonePutSerializer,
        }.get(self.request.method)


# ----------------------------------- Region Configuration City View ----------------------------------


class RegionConfigurationCityGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = RegionConfigurationCityModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["city_name"]
    filterset_class = RegionConfigurationCityFilter
    ordering = ["-core_generic_created_at"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = CITY_SUCCESS_MESSAGE

    def get_queryset(self):
        return RegionConfigurationCityModel.objects.with_details()

    def get_serializer_class(self):

        return {
            "GET": RegionConfigurationCityListModelSerializer,
            "POST": RegionConfigurationCityCreateModelSerializer,
            "PUT": RegionConfigurationCityPutSerializer,
        }.get(self.request.method)


# RegionConfigurationPincodeModel
# ----------------------------------- Region Configuration Pincode View ----------------------------------


class RegionConfigurationPincodeGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = RegionConfigurationPincodeModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RegionConfigurationPincodeFilter
    search_fields = ["pincode__pincode"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = PINCODE_SUCCESS_MESSAGE

    def get_queryset(self):
        qs = RegionConfigurationPincodeModel.objects.with_details()
        return qs.annotate(assigned_fo_count=Count("UserDetailModel_assigned_pincode"))

    def get_serializer_class(self):

        return {
            "GET": RegionConfigurationPincodeListModelSerializer,
            "POST": RegionConfigurationPincodeCreateModelSerializer,
            "PUT": RegionConfigurationPincodePutSerializer,
        }.get(self.request.method)


# ----------------------------------- Region Configuration Area View ----------------------------------


class RegionConfigurationAreaGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = RegionConfigurationAreaModel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RegionConfigurationAreaFilter
    search_fields = ["title"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = AREA_SUCCESS_MESSAGE

    def get_queryset(self):
        return RegionConfigurationAreaModel.objects.with_details()

    def get_serializer_class(self):

        return {
            "GET": RegionConfigurationAreaListModelSerializer,
            "POST": RegionConfigurationAreaCreateModelSerializer,
            "PUT": RegionConfigurationAreaPutSerializer,
        }.get(self.request.method)
