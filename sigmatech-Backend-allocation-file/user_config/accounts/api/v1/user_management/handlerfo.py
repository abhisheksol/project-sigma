from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import timedelta

from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.operations.case_management.models import CaseManagementCaseModel
from user_config.user_auth.models import UserModel
from store.configurations.fo_assignment_rules.models import (
    ConfigurationFOAssignmentRulesModel,
)
# __define-ocg__

class FoAssignmentHandler(CoreGenericBaseHandler):
    

    case_instance: CaseManagementCaseModel = None
    fo_user_instance: UserModel = None

    def validate(self):
        data = self.data  # comes from serializer
        case_id = data.get("case_id")
        fo_id = data.get("fo_id")
        print("-------------- FO Assignment Handler Initialized ----------------->>>>>")
        # Validate Case
        try:
            self.case_instance = CaseManagementCaseModel.objects.get(id=case_id)
        except CaseManagementCaseModel.DoesNotExist:
            raise ValidationError("Invalid Case ID provided.")

        # Validate FO User
        try:
            self.fo_user_instance = UserModel.objects.get(id=fo_id)
        except UserModel.DoesNotExist:
            raise ValidationError("Invalid FO ID provided.")

        # --- Check maximum case per day rule ---
        config = ConfigurationFOAssignmentRulesModel.objects.first()
        print(f"FO Assignment Config--------->: {config.no_of_max_cases_per_day}")
        if config and config.is_max_cases_per_day_enabled:

            print("Max cases per day rule is enabled.------------------>")
            # Count today's cases for this FO
            start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            current_case_count = CaseManagementCaseModel.objects.filter(
                assigned_user_for_field_operations=self.fo_user_instance,
                core_generic_created_at__gte=start_of_day,
                core_generic_created_at__lt=end_of_day
            ).count()

            print(f"Current case count for FO -------------->{self.fo_user_instance.id} today: {current_case_count}")

            if current_case_count >= config.no_of_max_cases_per_day:
                raise ValidationError(
                    f"FO {self.fo_user_instance.id} has already reached the daily limit of "
                    f"{config.no_of_max_cases_per_day} cases."
                )

    def create(self):
        with transaction.atomic():
            self.case_instance.assigned_user_for_field_operations = self.fo_user_instance
            self.case_instance.save()

            self.logger.info(
                f"Case {self.case_instance.id} assigned to FO {self.fo_user_instance.id}."
            )
