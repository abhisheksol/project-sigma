from typing import Dict, List, Optional, Any
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.fo_assignment_rules.api.v1.utils.constant import (
    FO_ASSIGNMENT_RULES_NOT_FOUND,
    INVALID_PINCODE_ID_ERROR_MESSAGE,
    INVALID_USER_ID_ERROR_MESSAGE,
)
from store.configurations.fo_assignment_rules.models import (
    ConfigurationFOAssignmentRuleGroupModel,
    ConfigurationFOAssignmentRulesModel,
    FOAssignmentRuleFOMappingModel,
    FOAssignmentRuleLocationMappingModel,
)
from django.db import transaction
from store.configurations.region_config.models import RegionConfigurationPincodeModel
from user_config.user_auth.models import UserModel
from store.configurations.fo_assignment_rules.enums import (
    PerformanceOptionalRuleTypeEnumChoices,
)


class FOAssignmentRulesUpdateHandler(CoreGenericBaseHandler):
    fo_key: Optional[str] = None
    loc_key: Optional[str] = None

    instance: ConfigurationFOAssignmentRulesModel

    def validate(self) -> Optional[None]:
        """
        Validate incoming FO assignment rule update payload.
        Ensures referenced user IDs and pincode IDs exist.
        """
        for rule in PerformanceOptionalRuleTypeEnumChoices:
            fo_key: str = f"{rule.value}_fo_mappings"
            loc_key: str = f"{rule.value}_location_mappings"

            for user_id in self.data.get(fo_key, []):
                if not UserModel.objects.filter(id=user_id).exists():
                    self.set_error_message(
                        INVALID_USER_ID_ERROR_MESSAGE.format(user_id), key="user_id"
                    )

            for pincode_id in self.data.get(loc_key, []):
                if not RegionConfigurationPincodeModel.objects.filter(
                    id=pincode_id
                ).exists():
                    self.set_error_message(
                        INVALID_PINCODE_ID_ERROR_MESSAGE.format(pincode_id),
                        key="pincode_id",
                    )

        try:
            self.instance = self.queryset.get()
        except ConfigurationFOAssignmentRulesModel.DoesNotExist:
            return self.set_error_message(FO_ASSIGNMENT_RULES_NOT_FOUND)

        return None

    def create(self) -> None:
        """
        Update or create FO assignment rules and related mappings.
        """
        with transaction.atomic():

            # update simple fields
            simple_fields: Dict[str, Any] = {
                k: v
                for k, v in self.data.items()
                if not any(
                    k.startswith(rule.value)
                    for rule in PerformanceOptionalRuleTypeEnumChoices
                )
            }
            for attr, value in simple_fields.items():
                setattr(self.instance, attr, value)
            self.instance.save()

            # build groups_data from flattened keys
            groups_data: List[Dict[str, Any]] = []
            for rule in PerformanceOptionalRuleTypeEnumChoices:
                rule_type: str = rule.value
                fo_key: str = f"{rule_type}_fo_mappings"
                loc_key: str = f"{rule_type}_location_mappings"

                if fo_key in self.data or loc_key in self.data:
                    groups_data.append(
                        {
                            "rule_type": rule_type,
                            "fo_mappings": self.data.get(fo_key, []),
                            "location_mappings": self.data.get(loc_key, []),
                        }
                    )

            # handle nested groups
            for group_data in groups_data:
                group, _ = (
                    ConfigurationFOAssignmentRuleGroupModel.objects.update_or_create(
                        rule_config=self.instance,
                        rule_type=group_data["rule_type"],
                        defaults={
                            "rule_config": self.instance,
                            "rule_type": group_data["rule_type"],
                        },
                    )
                )

                # reset & recreate FO mappings
                group.FOAssignmentRuleFOMappingModel_rule_group.all().delete()
                FOAssignmentRuleFOMappingModel.objects.bulk_create(
                    [
                        FOAssignmentRuleFOMappingModel(
                            rule_group=group, user_id=user_id
                        )
                        for user_id in group_data["fo_mappings"]
                    ]
                )

                # reset & recreate location mappings
                group.location_mappings.all().delete()
                FOAssignmentRuleLocationMappingModel.objects.bulk_create(
                    [
                        FOAssignmentRuleLocationMappingModel(
                            rule_group=group, pincode_id=pincode_id
                        )
                        for pincode_id in group_data["location_mappings"]
                    ]
                )
