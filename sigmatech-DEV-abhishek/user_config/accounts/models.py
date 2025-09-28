import uuid
from django.db import models
from typing import List
from django.db.models.query import QuerySet
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.user_auth.enums import BloodGroupEnum, EmergencyContactRelationEnum
from user_config.user_auth.models import UserModel
from django.db.models import Q

# Create your models here.


class UserDetailQuerySet(models.QuerySet):
    def filter_by_region(self, region_ids: List[str]) -> QuerySet:
        """
        Filters users who are directly or indirectly associated with the specified regions.

        This method retrieves users based on their regional assignments, combining multiple regions with OR logic:
        - SR_MANAGER: Users directly assigned to any of the specified regions.
        - MANAGER: Users assigned to zones within any of the specified regions.
        - SUPERVISOR: Users assigned to cities within zones of any of the specified regions.
        - FIELD_OFFICER: Users assigned to pincodes or areas within cities in zones of any of the specified regions.

        Args:
            region_ids: A list of UUIDs of the regions to filter users by.

        Returns:
            QuerySet: A filtered queryset containing users associated with any of the specified regions.
        """
        if not region_ids:
            return self

        # Initialize Q object for combining region filters
        region_query = Q()
        for region_id in region_ids:
            # SR_MANAGERS directly assigned to the region
            sr_managers = Q(assigned_region__id=region_id)
            # MANAGERS assigned to zones within the region
            managers = Q(assigned_zone__region__id=region_id)
            # SUPERVISORS assigned to cities within zones of the region
            supervisors = Q(assigned_city__zone__region__id=region_id)
            # FIELD_OFFICERS assigned to pincodes within cities in zones of the region
            field_officers_pincode = Q(
                assigned_pincode__city__zone__region__id=region_id
            )
            # FIELD_OFFICERS assigned to areas within pincodes in cities in zones of the region
            field_officers_area = Q(
                assigned_area__pincode__city__zone__region__id=region_id
            )
            # Combine conditions for this region with OR
            region_query |= (
                sr_managers
                | managers
                | supervisors
                | field_officers_pincode
                | field_officers_area
            )

        # Apply the combined region filters and ensure distinct results
        return self.filter(region_query).distinct()

    def filter_by_zone(self, zone_ids: List[str]) -> QuerySet:
        """
        Filters users who are directly or indirectly associated with the specified zones.

        This method retrieves users based on their zone assignments, combining multiple zones with OR logic:
        - MANAGER: Users directly assigned to any of the specified zones.
        - SUPERVISOR: Users assigned to cities within any of the specified zones.
        - FIELD_OFFICER: Users assigned to pincodes or areas within cities of any of the specified zones.

        Args:
            zone_ids: A list of UUIDs of the zones to filter users by.

        Returns:
            QuerySet: A filtered queryset containing users associated with any of the specified zones.
        """
        if not zone_ids:
            return self

        # Initialize Q object for combining zone filters
        zone_query = Q()
        for zone_id in zone_ids:
            # MANAGERS directly assigned to the zone
            managers = Q(assigned_zone__id=zone_id)
            # SUPERVISORS assigned to cities within the zone
            supervisors = Q(assigned_city__zone__id=zone_id)
            # FIELD_OFFICERS assigned to pincodes within cities of the zone
            field_officers_pincode = Q(assigned_pincode__city__zone__id=zone_id)
            # FIELD_OFFICERS assigned to areas within pincodes in cities of the zone
            field_officers_area = Q(assigned_area__pincode__city__zone__id=zone_id)
            # Combine conditions for this zone with OR
            zone_query |= (
                managers | supervisors | field_officers_pincode | field_officers_area
            )

        # Apply the combined zone filters and ensure distinct results
        return self.filter(zone_query).distinct()


class UserDetailModel(CoreGenericModel):
    user = models.OneToOneField(
        UserModel,
        primary_key=True,
        unique=True,
        related_name="UserDetailModel_user",
        on_delete=models.CASCADE,
        db_column="USER_AUTH_ID",
        editable=False,
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
    objects = UserDetailQuerySet.as_manager()

    class Meta:
        db_table = "USER_DETAIL_TABLE"

    def __str__(self):
        if self.user and self.user.username:
            return self.user.username
        elif self.user:
            return f"User {self.user.id}"
        else:
            return "User Detail (No User)"


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
