import uuid
from django.db import models

from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.models import LoanConfigurationsProductAssignmentModel
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.user_auth.enums import BloodGroupEnum, EmergencyContactRelationEnum
from user_config.user_auth.models import UserModel

# Create your models here.


class UserDetailModel(CoreGenericModel):
    user = models.OneToOneField(
        UserModel,
        primary_key=True,
        unique=True,
        related_name="UserDetailModel_user",
        on_delete=models.CASCADE,
        db_column="USER_AUTH_ID",
        # editable=False,
    )

    profile_picture = models.URLField(
        max_length=1000, null=True, blank=True, db_column="PROFILE_PICTURE"
    )

    blood_group = models.CharField(
        max_length=20,
        choices=BloodGroupEnum.choices(),
        db_column="BLOOD_GROUP",
        null=True,
        blank=True,
    )

    vehicle_number = models.CharField(
        max_length=100, db_column="VEHICLE", null=True, blank=True
    )
    emergency_phone_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column="EMERGENCY_PHONE_NUMBER",
    )
    emergency_contact_relation_name = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=EmergencyContactRelationEnum.choices(),
        db_column="EMERGENCY_CONTACT_RELATION_NAME",
    )
    emergency_contact_relation = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=EmergencyContactRelationEnum.choices(),
        db_column="EMERGENCY_CONTACT_RELATION",
    )

    # sr manager are assigned to entire Region
    assigned_region = models.ManyToManyField(
        RegionConfigurationRegionModel,
        blank=True,
        related_name="UserDetailModel_assigned_region",
        db_column="ASSIGNED_REGION_ID",
    )
    # manager are assigned to entire zone
    assigned_zone = models.ManyToManyField(
        RegionConfigurationZoneModel,
        blank=True,
        related_name="UserDetailModel_assigned_zone",
        db_column="ASSIGNED_ZONE_ID",
    )
    # supervisor are assigned to entire one or more than one city
    assigned_city = models.ManyToManyField(
        RegionConfigurationCityModel,
        blank=True,
        related_name="UserDetailModel_assigned_city",
        db_column="ASSIGNED_ZONE_ID",
    )
    # field agent's are assigned to one or more than one pincode or area

    assigned_pincode = models.ManyToManyField(
        RegionConfigurationPincodeModel,
        blank=True,
        related_name="UserDetailModel_assigned_pincode",
        db_column="ASSIGNED_PINCODE_ID",
    )

    assigned_area = models.ManyToManyField(
        RegionConfigurationAreaModel,
        blank=True,
        related_name="UserDetailModel_assigned_area",
        db_column="ASSIGNED_AREA_ID",
    )

    class Meta:
        db_table = "USER_DETAIL_TABLE"

    def __str__(self):
        if self.user and hasattr(self.user, 'username'):
            return str(self.user.username or "")
        return "User Detail"
 

class UserAssignedProdudctsModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="USER_ASSIGNED_PRODUCTS__ID",
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="UserAssignedProdudctsModel_user",
        db_column="USER_AUTH_ID",
        # editable=False,
    )
    product_assignment = models.ForeignKey(
        LoanConfigurationsProductAssignmentModel,
        on_delete=models.CASCADE,
        related_name="UserAssignedProdudctsModel_product_assignment",
        db_column="PRODUCT_ASSIGNMENT_ID",
    )

    class Meta:
        db_table = "USER_ASSIGNED_PRODUCTS_TABLE"
        unique_together = ("user", "product_assignment")
