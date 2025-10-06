from rest_framework import serializers
from store.configurations.fo_assignment_rules.api.v1.utils.enum import TabNameEnum
from store.configurations.fo_assignment_rules.api.v1.utils.fo_assignement_resethandler import (
    FOAssignmentRulesResetHandler,
)
from store.configurations.fo_assignment_rules.api.v1.utils.fo_assignement_updatehandler import (
    FOAssignmentRulesUpdateHandler,
)

from store.configurations.fo_assignment_rules.models import (
    ConfigurationFOAssignmentRuleGroupModel,
    ConfigurationFOAssignmentRulesModel,
    FOAssignmentRuleFOMappingModel,
    FOAssignmentRuleLocationMappingModel,
)

from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from store.configurations.fo_assignment_rules.enums import (
    PerformanceOptionalRuleTypeEnumChoices,
)
from django.db.models.query import QuerySet
from typing import List


class FOAssignmentRuleFOMappingSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = FOAssignmentRulesUpdateHandler
    user_id = serializers.UUIDField(source="user.id")

    class Meta:
        model = FOAssignmentRuleFOMappingModel
        fields = ["id", "user_id"]


class FOAssignmentRuleLocationMappingSerializer(serializers.ModelSerializer):
    pincode_id = serializers.UUIDField()

    handler_class = FOAssignmentRulesUpdateHandler

    class Meta:
        model = FOAssignmentRuleLocationMappingModel
        fields = ["id", "pincode_id"]


class ConfigurationFOAssignmentRuleGroupSerializer(serializers.ModelSerializer):
    fo_mappings = FOAssignmentRuleFOMappingSerializer(many=True, required=False)
    location_mappings = FOAssignmentRuleLocationMappingSerializer(
        many=True, required=False
    )
    handler_class = FOAssignmentRulesUpdateHandler

    class Meta:
        model = ConfigurationFOAssignmentRuleGroupModel
        fields = ["id", "rule_type", "fo_mappings", "location_mappings"]


class ConfigurationFOAssignmentRulesSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):

    # rule_groups = ConfigurationFOAssignmentRuleGroupSerializer(
    #     many=True, required=False)
    OPTIONAL_MEDIA_UPLOAD_fo_mappings = serializers.SerializerMethodField()
    OPTIONAL_MEDIA_UPLOAD_location_mappings = serializers.SerializerMethodField()
    OPTIONAL_GPS_TRACKING_fo_mappings = serializers.SerializerMethodField()
    OPTIONAL_GPS_TRACKING_location_mappings = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurationFOAssignmentRulesModel
        fields = [
            "id",
            "is_exclude_inactive_fos_enabled",
            "no_of_exclude_inactive_fos_days",
            "is_restrict_by_proximity_enabled",
            "no_of_restrict_by_proximity_km",
            "is_avoid_reassign_same_pincode_enabled",
            "is_max_cases_per_day_enabled",
            "no_of_max_cases_per_day",
            "is_high_priority_to_top_fos_enabled",
            "performance_metric",
            "performance_threshold",
            "is_avoid_reassign_failed_cases_enabled",
            "no_of_failed_attempts_threshold",
            "OPTIONAL_MEDIA_UPLOAD_fo_mappings",
            "OPTIONAL_MEDIA_UPLOAD_location_mappings",
            "OPTIONAL_GPS_TRACKING_fo_mappings",
            "OPTIONAL_GPS_TRACKING_location_mappings",
        ]

    def get_OPTIONAL_MEDIA_UPLOAD_fo_mappings(self, obj):
        try:
            rule_instance: ConfigurationFOAssignmentRuleGroupModel = (
                ConfigurationFOAssignmentRuleGroupModel.objects.get(
                    rule_config=obj,
                    rule_type=PerformanceOptionalRuleTypeEnumChoices.OPTIONAL_MEDIA_UPLOAD.value,
                )
            )
            assigned_fo_mapping_rules_queryset: QuerySet[
                FOAssignmentRuleFOMappingModel
            ] = rule_instance.FOAssignmentRuleFOMappingModel_rule_group.all()
            fo_user_id_list: List[str] = assigned_fo_mapping_rules_queryset.values_list(
                "user__pk", flat=True
            )
            return fo_user_id_list
        except ConfigurationFOAssignmentRuleGroupModel.DoesNotExist:
            return []

    def get_OPTIONAL_MEDIA_UPLOAD_location_mappings(self, obj):
        try:
            rule_instance = ConfigurationFOAssignmentRuleGroupModel.objects.get(
                rule_config=obj,
                rule_type=PerformanceOptionalRuleTypeEnumChoices.OPTIONAL_MEDIA_UPLOAD.value,
            )
            qs: QuerySet[FOAssignmentRuleLocationMappingModel] = (
                rule_instance.location_mappings.all()
            )
            return list(qs.values_list("pincode__pk", flat=True))
        except ConfigurationFOAssignmentRuleGroupModel.DoesNotExist:
            return []

    def get_OPTIONAL_GPS_TRACKING_fo_mappings(self, obj):
        try:
            rule_instance = ConfigurationFOAssignmentRuleGroupModel.objects.get(
                rule_config=obj,
                rule_type=PerformanceOptionalRuleTypeEnumChoices.OPTIONAL_GPS_TRACKING.value,
            )
            qs = rule_instance.FOAssignmentRuleFOMappingModel_rule_group.all()
            return list(qs.values_list("user__pk", flat=True))
        except ConfigurationFOAssignmentRuleGroupModel.DoesNotExist:
            return []

    def get_OPTIONAL_GPS_TRACKING_location_mappings(self, obj):
        try:
            rule_instance = ConfigurationFOAssignmentRuleGroupModel.objects.get(
                rule_config=obj,
                rule_type=PerformanceOptionalRuleTypeEnumChoices.OPTIONAL_GPS_TRACKING.value,
            )
            qs = rule_instance.location_mappings.all()
            return list(qs.values_list("pincode__pk", flat=True))
        except ConfigurationFOAssignmentRuleGroupModel.DoesNotExist:
            return []


class ConfigurationFOAssignmentRulesPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = FOAssignmentRulesUpdateHandler

    id = serializers.UUIDField(required=True)
    is_exclude_inactive_fos_enabled = serializers.BooleanField(required=False)
    no_of_exclude_inactive_fos_days = serializers.IntegerField(required=False)
    is_restrict_by_proximity_enabled = serializers.BooleanField(required=False)
    no_of_restrict_by_proximity_km = serializers.IntegerField(required=False)
    is_max_cases_per_day_enabled = serializers.BooleanField(required=False)
    no_of_max_cases_per_day = serializers.IntegerField(required=False)
    is_high_priority_to_top_fos_enabled = serializers.BooleanField(required=False)
    performance_metric = serializers.CharField(required=False)
    performance_threshold = serializers.FloatField(required=False)
    is_avoid_reassign_failed_cases_enabled = serializers.BooleanField(required=False)
    no_of_failed_attempts_threshold = serializers.IntegerField(required=False)
    is_avoid_reassign_same_pincode_enabled = serializers.BooleanField(required=False)

    #  Flattened fields for each rule_type
    for rule in PerformanceOptionalRuleTypeEnumChoices:
        locals()[f"{rule.value}_fo_mappings"] = serializers.ListField(
            child=serializers.UUIDField(), required=False
        )
        locals()[f"{rule.value}_location_mappings"] = serializers.ListField(
            child=serializers.UUIDField(), required=False
        )

    queryset = ConfigurationFOAssignmentRulesModel.objects.all()


class FOAssignmentRulesResetSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = FOAssignmentRulesResetHandler
    tab_name = serializers.ChoiceField(
        choices=[(tag.value, tag.name) for tag in TabNameEnum],
        # help_text="Which tab to reset: eligibility | priority | visit_docs"
    )
    queryset = ConfigurationFOAssignmentRulesModel.objects.all()
