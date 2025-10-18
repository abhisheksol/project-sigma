from django.db import transaction
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler


class FOAssignmentRulesResetHandler(CoreGenericBaseHandler):

    DEFAULTS = {
        "eligibility": {
            "is_exclude_inactive_fos_enabled": False,
            "no_of_exclude_inactive_fos_days": 7,
            "is_restrict_by_proximity_enabled": False,
            "no_of_restrict_by_proximity_km": 15,
            "is_max_cases_per_day_enabled": False,
            "no_of_max_cases_per_day": 15,
        },
        "priority": {
            "is_high_priority_to_top_fos_enabled": False,
            "performance_metric": "RECOVERY_RATE",
            "performance_threshold": 80.0,
            "is_avoid_reassign_failed_cases_enabled": False,
            "no_of_failed_attempts_threshold": 3,
        },
        "visit_docs": {
            "fo_mappings": [],
            "location_mappings": [],
        },
    }

    def validate(self):
        """
        Validate reset request.
        """
        tab_name = self.data.get("tab_name")
        if not tab_name:
            return self.set_error_message("Missing field: tab_name")
        if tab_name not in self.DEFAULTS:
            return self.set_error_message(f"Invalid tab_name: {tab_name}")

        if not self.queryset.exists():
            return self.set_error_message("Configuration not found.")

    def create(self):
        """
        Perform reset operation for a given tab.
        """
        instance = self.queryset.first()
        tab_name = self.data.get("tab_name")

        with transaction.atomic():
            if tab_name == "eligibility":
                for field, default in self.DEFAULTS["eligibility"].items():
                    setattr(instance, field, default)
                instance.save()

            elif tab_name == "priority":
                for field, default in self.DEFAULTS["priority"].items():
                    setattr(instance, field, default)
                instance.save()

            elif tab_name == "visit_docs":
                # clear mappings across all groups
                for group in instance.rule_groups.all():
                    group.FOAssignmentRuleFOMappingModel_rule_group.all().delete()
                    group.location_mappings.all().delete()

        return instance
