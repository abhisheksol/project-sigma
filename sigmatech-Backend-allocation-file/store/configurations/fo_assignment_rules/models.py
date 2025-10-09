import uuid
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.fo_assignment_rules.enums import (
    PerformanceMetricsFactorEnumChoices,
    PerformanceOptionalRuleTypeEnumChoices,
)
from user_config.user_auth.models import UserModel
from store.configurations.region_config.models import RegionConfigurationPincodeModel

# Create your models here.


class ConfigurationFOAssignmentRulesManager(models.Manager):
    def get(self):
        obj, created = self.get_or_create(id=uuid.uuid4())
        return obj


class ConfigurationFOAssignmentRulesModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="FO_ASSIGNMENT_RULE_ID",
        default=uuid.uuid4,
    )
    is_exclude_inactive_fos_enabled = models.BooleanField(
        default=False, db_column="IS_EXCLUDE_INACTIVE_FOS_ENABLED"
    )
    no_of_exclude_inactive_fos_days = models.IntegerField(
        default=7, db_column="NO_OF_EXCLUDE_INACTIVE_FO_DAYS"
    )

    is_restrict_by_proximity_enabled = models.BooleanField(
        default=False, db_column="IS_RESTRICTION_BY_PROXIMITY_ENABLED"
    )
    no_of_restrict_by_proximity_km = models.IntegerField(
        default=15, db_column="NO_OF_RESTRICT_BY_PEROMIXITY_KM"
    )

    is_max_cases_per_day_enabled = models.BooleanField(
        default=False, db_column="IS_MAX_CASES_PER_DAY_ENABLED"
    )
    no_of_max_cases_per_day = models.IntegerField(
        default=1, db_column="NO_OF_MAX_CASES_PER_DAY"
    )

    is_high_priority_to_top_fos_enabled = models.BooleanField(
        default=False, db_column="IS_HIGH_PRIORITY_TO_TOP_FOS_ENABLED"
    )
    performance_metric = models.CharField(
        max_length=50,
        choices=PerformanceMetricsFactorEnumChoices.choices(),
        default=PerformanceMetricsFactorEnumChoices.RECOVERY_RATE.value,
        db_column="PERFORMANCE_METRICS_FACTOR",
    )
    performance_threshold = models.FloatField(
        default=80.0, db_column="PERFORMANCE_THRESHOLD"
    )

    is_avoid_reassign_failed_cases_enabled = models.BooleanField(
        default=False, db_column="IS_AVOID_REASSIGN_FAILED_CASES_ENABLED"
    )
    no_of_failed_attempts_threshold = models.PositiveIntegerField(
        default=3, db_column="NO_OF_FAILED_ATTEMPTS_THRESHOLD"
    )
    # apply even if in same pincode
    is_avoid_reassign_same_pincode_enabled = models.BooleanField(
        default=False, db_column="IS_AVOID_REASSIGN_SAME_PINCODE_ENABLED"
    )
    objects: ConfigurationFOAssignmentRulesManager = (
        ConfigurationFOAssignmentRulesManager
    )

    def save(self, *args, **kwargs):
        if not self.pk and ConfigurationFOAssignmentRulesModel.objects.exists():
            raise ValueError(
                "Only one ConfigurationFOAssignmentRulesModel instance is allowed."
            )
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "FO_ASSIGNMENT_RULE_TABLE"


# ---------------------------
#  Rule Groups
# ---------------------------
class ConfigurationFOAssignmentRuleGroupModel(CoreGenericModel):
    """
    A group that represents one type of FO assignment rule
    (e.g., optional media upload, optional GPS tracking).
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="FO_ASSIGNMENT_RULE_GROUP_ID",
        default=uuid.uuid4,
    )

    # FK to global config
    rule_config = models.ForeignKey(
        ConfigurationFOAssignmentRulesModel,
        on_delete=models.CASCADE,
        related_name="rule_groups",
        db_column="FO_ASSIGNMENT_RULE_ID",
    )

    # e.g. "MEDIA_UPLOAD", "GPS_TRACKING", "GPS_LOCATION", "MEDIA_LOCATION"
    rule_type = models.CharField(
        max_length=50,
        choices=PerformanceOptionalRuleTypeEnumChoices.choices(),
        db_column="RULE_TYPE",
    )

    class Meta:
        db_table = "FO_ASSIGNMENT_RULE_GROUP_TABLE"
        unique_together = ("rule_config", "rule_type")


# ---------------------------
#  FO Mappings
# ---------------------------
class FOAssignmentRuleFOMappingModel(CoreGenericModel):
    """
    Map FOs to a specific rule group (e.g. FOs with optional media upload).
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_column="FO_ASSIGNMENT_RULE_FO_MAPPING_ID",
    )

    rule_group = models.ForeignKey(
        ConfigurationFOAssignmentRuleGroupModel,
        on_delete=models.CASCADE,
        related_name="FOAssignmentRuleFOMappingModel_rule_group",
        db_column="FO_ASSIGNMENT_RULE_GROUP_ID",
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="FOAssignmentRuleFOMappingModel_user",
        db_column="OPTIONAL_FO_ID",
    )

    class Meta:
        db_table = "FO_ASSIGNMENT_RULE_FO_MAPPING_TABLE"
        unique_together = ("rule_group", "user")


class FOAssignmentRuleLocationMappingModel(CoreGenericModel):
    """
    Map Locations to a specific rule group (e.g. Locations with optional GPS).
    """

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_column="FO_ASSIGNMENT_RULE_LOCATION_MAPPING_ID",
    )

    rule_group = models.ForeignKey(
        ConfigurationFOAssignmentRuleGroupModel,
        on_delete=models.CASCADE,
        related_name="location_mappings",
        db_column="FO_ASSIGNMENT_RULE_GROUP_ID",
    )

    pincode = models.ForeignKey(
        RegionConfigurationPincodeModel,
        on_delete=models.CASCADE,
        related_name="FOAssignmentRuleLocationMappingModel_pincode",
        db_column="OPTIONAL_PINCODE_ID",
    )

    class Meta:
        db_table = "FO_ASSIGNMENT_RULE_LOCATION_MAPPING_TABLE"
        unique_together = ("rule_group", "pincode")
