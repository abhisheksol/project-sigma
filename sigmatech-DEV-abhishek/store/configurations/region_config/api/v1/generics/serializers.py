from rest_framework import serializers
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationarea_create_handler import (
    RegionConfigurationAreaCreateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationarea_update_handler import (
    RegionConfigurationAreaUpdateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationcity_create_handler import (
    RegionConfigurationCityCreateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfiguration_create_handler import (
    RegionCOnfigurationCreateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfiguration_update_handler import (
    RegionConfigurationUpdateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationcity_updatehandler import (
    RegionConfigurationCityUpdateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationpincode_create_handler import (
    RegionConfigurationPincodeCreateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationpincode_update_handler import (
    RegionConfigurationPincodeUpdateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationzone_create_handler import (
    RegionConfigurationZoneCreateHandler,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationzone_update_handler import (
    RegionConfigurationZoneUpdateHandler,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)


# ----------------------------------- Region Configuration Serializers ----------------------------------
class RegionConfigurationRegionListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = RegionCOnfigurationCreateHandler

    # Try to get from annotations first, fallback to SerializerMethodField
    number_of_zones = serializers.SerializerMethodField()
    number_of_cities = serializers.SerializerMethodField()
    number_of_pincodes = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationRegionModel
        fields = [
            "id",
            "title",
            "description",
            "status",
            "number_of_zones",
            "number_of_cities",
            "number_of_pincodes",
        ]

    def get_number_of_zones(self, obj):
        # Try to get from annotation first
        if hasattr(obj, "number_of_zones"):
            return obj.number_of_zones
        # Fallback to manual count
        return obj.RegionConfigurationZoneModel_region.count()

    def get_number_of_cities(self, obj):
        # Try to get from annotation first
        if hasattr(obj, "number_of_cities"):
            return obj.number_of_cities
        # Fallback to manual count
        return RegionConfigurationCityModel.objects.filter(zone__region=obj).count()

    def get_number_of_pincodes(self, obj):
        # Try to get from annotation first
        if hasattr(obj, "number_of_pincodes"):
            return obj.number_of_pincodes
        # Fallback to manual count
        return RegionConfigurationPincodeModel.objects.filter(
            city__zone__region=obj
        ).count()


class RegionConfigurationRegionCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = RegionCOnfigurationCreateHandler

    class Meta:
        model = RegionConfigurationRegionModel
        fields = ["title", "status", "description"]


class RegionConfigurationRegionPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = RegionConfigurationUpdateHandler
    id = serializers.UUIDField()
    title = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    queryset = RegionConfigurationRegionModel.objects.all()


# ----------------------------------- Region Configuration Zone Serializers ----------------------------------
class RegionConfigurationZoneListModelSerializer(serializers.ModelSerializer):
    handler_class = RegionConfigurationZoneCreateHandler

    associated_region = serializers.CharField(read_only=True)
    number_of_cities = serializers.IntegerField(read_only=True)
    number_of_pincodes = serializers.IntegerField(read_only=True)
    number_of_areas = serializers.IntegerField(read_only=True)

    class Meta:
        model = RegionConfigurationZoneModel
        fields = [
            "id",
            "title",
            "description",
            "region",
            "status",
            "associated_region",
            "number_of_cities",
            "number_of_pincodes",
            "number_of_areas",
        ]


class RegionConfigurationZoneCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    region = serializers.UUIDField()
    handler_class = RegionConfigurationZoneCreateHandler

    class Meta:
        model = RegionConfigurationZoneModel
        fields = ["title", "region", "description"]


class RegionConfigurationZonePutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = RegionConfigurationZoneUpdateHandler
    id = serializers.UUIDField()
    title = serializers.CharField(required=False, allow_blank=True)
    region = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    queryset = RegionConfigurationZoneModel.objects.all()


# ----------------------------------- Region Configuration City Serializers ----------------------------------


class RegionConfigurationCityListModelSerializer(serializers.ModelSerializer):
    handler_class = RegionConfigurationCityCreateHandler

    zone_name = serializers.CharField(read_only=True)
    region_id = serializers.CharField(source="zone.region.id", read_only=True)
    associated_region = serializers.CharField(read_only=True)
    number_of_cities = serializers.IntegerField(read_only=True)
    number_of_pincodes = serializers.IntegerField(read_only=True)
    number_of_areas = serializers.IntegerField(read_only=True)

    city_name = serializers.CharField(read_only=True)

    class Meta:
        model = RegionConfigurationCityModel
        fields = [
            "id",
            "city_name",
            "zone",
            "region_id",
            "zone_name",
            "associated_region",
            "number_of_cities",
            "number_of_pincodes",
            "number_of_areas",
            "status",
            "description",
        ]


class RegionConfigurationCityCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    zone = serializers.UUIDField()
    city_name = serializers.CharField()
    handler_class = RegionConfigurationCityCreateHandler

    class Meta:
        model = RegionConfigurationCityModel
        fields = ["city_name", "description", "status", "zone"]


class RegionConfigurationCityPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = RegionConfigurationCityUpdateHandler
    id = serializers.UUIDField()
    city_name = serializers.CharField(required=False)
    zone = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    queryset = RegionConfigurationCityModel.objects.all()


# ----------------------------------- Region Configuration Pincode Serializers ----------------------------------


class RegionConfigurationPincodeListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = RegionConfigurationPincodeCreateHandler

    city_name = serializers.SerializerMethodField()
    zone_name = serializers.SerializerMethodField()
    region_name = serializers.SerializerMethodField()
    area_count = serializers.SerializerMethodField()
    zone = serializers.UUIDField(source="city.zone.id", read_only=True)
    pincode_value = serializers.CharField(source="pincode", read_only=True)
    assigned_fo_count = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = [
            "id",
            "pincode",
            "city",
            "city_name",
            "zone_name",
            "region_name",
            "area_count",
            "zone",
            "pincode_value",
            "status",
            "assigned_fo_count",
        ]

    def get_city_name(self, obj):
        return getattr(obj, "city_name", None)

    def get_zone_name(self, obj):
        return getattr(obj, "zone_name", None)

    def get_region_name(self, obj):
        return getattr(obj, "region_name", None)

    def get_area_count(self, obj):
        return getattr(obj, "area_count", 0)

    def get_assigned_fo_count(self, obj):
        value = getattr(obj, "assigned_fo_count", 0)
        return "OGL" if value == 0 else value


class RegionConfigurationPincodeCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    zone = serializers.UUIDField(write_only=True)
    city = serializers.UUIDField(write_only=True)
    pincode = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    handler_class = RegionConfigurationPincodeCreateHandler

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = ["zone", "city", "pincode"]


class RegionConfigurationPincodePutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = RegionConfigurationPincodeUpdateHandler
    id = serializers.UUIDField()
    pincode = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    city = serializers.UUIDField(required=False)
    queryset = RegionConfigurationPincodeModel.objects.all()


# ----------------------------------- Region Configuration Area Serializers ----------------------------------


class RegionConfigurationAreaListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = RegionConfigurationAreaCreateHandler
    city = serializers.UUIDField(source="pincode.city.id", read_only=True)
    city_name = serializers.CharField(read_only=True)
    zone_name = serializers.CharField(read_only=True)
    region_name = serializers.CharField(read_only=True)
    pincode_name = serializers.CharField(read_only=True)

    class Meta:
        model = RegionConfigurationAreaModel
        fields = [
            "id",
            "title",
            "city",
            "status",
            "pincode",
            "pincode_name",
            "city_name",
            "zone_name",
            "region_name",
        ]


class RegionConfigurationAreaCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    city = serializers.UUIDField()
    pincode = serializers.UUIDField()
    handler_class = RegionConfigurationAreaCreateHandler

    class Meta:
        model = RegionConfigurationAreaModel
        fields = ["title", "city", "pincode"]


class RegionConfigurationAreaPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = RegionConfigurationAreaUpdateHandler
    id = serializers.UUIDField()
    status = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    pincode = serializers.UUIDField(required=False)
    queryset = RegionConfigurationAreaModel.objects.all()
