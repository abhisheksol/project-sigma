from django.db import models
from core_utils.region_data.models import PincodeModel
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid

from store.configurations.region_config.queryset import (
    AreaQuerySet,
    CityQuerySet,
    PincodeQuerySet,
    RegionQuerySet,
    ZoneQuerySet,
)


class RegionConfigurationRegionModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, db_column="REGION_ID"
    )
    title = models.CharField(max_length=50, unique=True, db_column="REGION")
    description = models.CharField(
        max_length=100, null=True, blank=True, db_column="DESCRIPTION"
    )
    objects = RegionQuerySet.as_manager()

    class Meta:
        db_table = "REGION_TABLE"
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class RegionConfigurationZoneModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, db_column="ZONE_ID"
    )
    title = models.CharField(max_length=100, unique=True, db_column="ZONE")
    region = models.ForeignKey(
        RegionConfigurationRegionModel,
        on_delete=models.CASCADE,
        related_name="RegionConfigurationZoneModel_region",
        db_column="REGION_ID",
    )
    description = models.CharField(
        max_length=100, null=True, blank=True, db_column="DESCRIPTION"
    )
    objects = ZoneQuerySet.as_manager()

    class Meta:
        db_table = "ZONE_TABLE"
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class RegionConfigurationCityModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, db_column="CITY_ID"
    )
    city_name = models.CharField(
        max_length=50,
        null=True,
        db_column="CITY_NAME",
    )
    zone = models.ForeignKey(
        RegionConfigurationZoneModel,
        related_name="RegionConfigurationCityModel_zone",
        on_delete=models.CASCADE,
        db_column="ZONE_ID",
    )
    description = models.CharField(
        max_length=100, null=True, blank=True, db_column="DESCRIPTION"
    )
    objects = CityQuerySet.as_manager()

    class Meta:
        db_table = "CITY_TABLE"
        indexes = [
            models.Index(fields=["zone"]),
            models.Index(fields=["city_name"]),
        ]

    def __str__(self):
        return self.city_name


class RegionConfigurationPincodeModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, db_column="PINCODE_ID"
    )
    pincode = models.OneToOneField(
        PincodeModel,
        on_delete=models.CASCADE,
        related_name="RegionConfigurationPincodeModel_pincode",
        db_column="PINCODE",
    )
    city = models.ForeignKey(
        RegionConfigurationCityModel,
        on_delete=models.CASCADE,
        db_column="CITY_ID",
        related_name="RegionConfigurationPincodeModel_city",
    )

    objects = PincodeQuerySet.as_manager()

    class Meta:
        db_table = "PINCODE_TABLE"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["pincode"]),
        ]

    def __str__(self):
        return self.pincode.pincode


class RegionConfigurationAreaModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False, db_column="AREA_ID"
    )
    title = models.CharField(max_length=255, db_column="AREA_NAME")
    pincode = models.ForeignKey(
        RegionConfigurationPincodeModel,
        on_delete=models.CASCADE,
        db_column="PINCODE_ID",
        related_name="RegionConfigurationAreaModel_pincode",
    )

    objects = AreaQuerySet.as_manager()

    class Meta:
        db_table = "AREA_TABLE"
        unique_together = ("title", "pincode")
        indexes = [
            models.Index(fields=["pincode"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title
