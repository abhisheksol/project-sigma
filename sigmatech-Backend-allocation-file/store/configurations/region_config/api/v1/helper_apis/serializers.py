from rest_framework import serializers
from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericHelperAPISerializerMethodField,
)
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationAreaModel,
)
from core_utils.region_data.models import CityModel, PincodeModel


class RegionConfigurationRegionListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationRegionModel
        fields = ["value", "label", "disabled"]


class RegionConfigurationZoneListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationZoneModel
        fields = ["value", "label", "disabled"]


class RegionConfigurationAllCityListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):

    value = serializers.CharField(source="id", read_only=True)
    label = serializers.CharField(source="name", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = CityModel
        fields = ["value", "label", "disabled"]

    def get_disabled(self, obj):
        if RegionConfigurationCityModel.objects.filter(city_name=obj).exists():
            return True
        return False


class RegionConfigurationCityListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    disabled = serializers.SerializerMethodField()
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="city_name", read_only=True)

    class Meta:
        model = RegionConfigurationCityModel
        fields = ["value", "label", "disabled"]


class RegionConfigurationPincodeListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="pincode", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = RegionConfigurationPincodeModel
        fields = ["value", "label", "disabled"]


class RegionConfigurationAreaListHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    disabled = serializers.SerializerMethodField()
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)

    class Meta:
        model = RegionConfigurationAreaModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


# --------------------------------------- All India Pincode List ---------------------------------------


class RegionConfigurationAllIndiaPincodeListHelperModelSerializer(
    serializers.ModelSerializer
):

    disabled = serializers.SerializerMethodField()
    label = serializers.CharField(source="pincode", read_only=True)
    value = serializers.CharField(source="pincode", read_only=True)

    class Meta:
        model = PincodeModel
        fields = ["value", "label", "disabled"]

    def get_disabled(self, obj):
        if RegionConfigurationPincodeModel.objects.filter(pincode=obj).exists():
            return True
        return False
