from core_utils.region_data.models import CityModel, PincodeModel
from core_utils.utils.generics.views.generic_views import CoreGenericGetAPIView
from rest_framework import generics, permissions
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)

from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)

from store.configurations.region_config.api.v1.helper_apis.serializers import (
    RegionConfigurationAllCityListHelperModelSerializer,
    RegionConfigurationAllIndiaPincodeListHelperModelSerializer,
    RegionConfigurationCityListHelperModelSerializer,
    RegionConfigurationRegionListHelperModelSerializer,
    RegionConfigurationZoneListHelperModelSerializer,
    RegionConfigurationPincodeListHelperModelSerializer,
    RegionConfigurationAreaListHelperModelSerializer,
)

# ---------------------------------------Region hepler View------------------------------------


class RegionConfigurationRegionHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RegionConfigurationRegionModel.objects.all()

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationRegionListHelperModelSerializer,
        }.get(self.request.method)


# ---------------------------------------Zone hepler View------------------------------------


class RegionConfigurationZoneHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RegionConfigurationZoneModel.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        region_ids = self.request.query_params.get("region")

        if region_ids:
            # convert "id1,id2,id3" → ["id1", "id2", "id3"]
            region_ids = region_ids.split(",")
            queryset = queryset.filter(region_id__in=region_ids)

        return queryset

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationZoneListHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------ALL city name Range Helper API View--------------------------------


class RegionConfigurationAllCityHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CityModel.objects.select_related("state", "country", "pincode").all()

    def get_queryset(self):
        queryset = super().get_queryset()

        #  search by name (at least 3 chars)
        search = self.request.GET.get("search")
        if search and len(search) >= 3:
            queryset = queryset.filter(name__istartswith=search)

        #  filter by zone_id (single or multiple)
        zone_ids = self.request.query_params.get("zone")
        if zone_ids:
            zone_ids = zone_ids.split(",")
            queryset = queryset.filter(zone_id__in=zone_ids)

        #  optional: filter by region_id via relation
        region_ids = self.request.query_params.get("region")
        if region_ids:
            region_ids = region_ids.split(",")
            queryset = queryset.filter(zone__region_id__in=region_ids)

        return queryset

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationAllCityListHelperModelSerializer,
        }.get(self.request.method)


# ---------------------------------------city hepler View-----------------------------


class RegionConfigurationCityHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = RegionConfigurationCityModel.objects.all()

        zone_ids = self.request.query_params.get("zone_id")
        if zone_ids:
            # split "id1,id2,id3" → ["id1", "id2", "id3"]
            zone_ids = [z.strip() for z in zone_ids.split(",") if z.strip()]
            queryset = queryset.filter(zone_id__in=zone_ids)

        return queryset

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationCityListHelperModelSerializer,
        }.get(self.request.method)


# ---------------------------------------Pincode hepler View-----------------------------


class RegionConfigurationPincodeHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RegionConfigurationPincodeModel.objects.all()

    def get_queryset(self):
        queryset = RegionConfigurationPincodeModel.objects.all()

        city_ids = self.request.query_params.get("city_id")
        if city_ids:
            # split "id1,id2,id3" → ["id1", "id2", "id3"]
            city_ids = [c.strip() for c in city_ids.split(",") if c.strip()]
            queryset = queryset.filter(city_id__in=city_ids)

        return queryset

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationPincodeListHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------Area Helper API View--------------------------------


class RegionConfigurationAreaHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RegionConfigurationAreaModel.objects.all()

    def get_queryset(self):
        queryset = RegionConfigurationAreaModel.objects.all()

        pincode_ids = self.request.query_params.get("pincode_id")
        if pincode_ids:
            # split "id1,id2,id3" → ["id1", "id2", "id3"]
            pincode_ids = [p.strip() for p in pincode_ids.split(",") if p.strip()]
            queryset = queryset.filter(pincode_id__in=pincode_ids)

        return queryset

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationAreaListHelperModelSerializer,
        }.get(self.request.method)


# --------------------------------PincodeRange Helper API View--------------------------------


class RegionConfigurationPincodeRangeHelperGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PincodeModel.objects.all()

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search and len(search) >= 3:
            return self.queryset.filter(pincode__istartswith=search)
        return self.queryset.none()

    def get_serializer_class(self):
        return {
            "GET": RegionConfigurationAllIndiaPincodeListHelperModelSerializer,
        }.get(self.request.method)
