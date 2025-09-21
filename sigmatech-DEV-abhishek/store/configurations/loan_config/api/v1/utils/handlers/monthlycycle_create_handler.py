from django.db import transaction
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.loan_config.api.v1.utils.constants import (
    MONTHLY_CYCLE_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
    MONTHLY_CYCLE_TITLE_REQUIRED_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import LoanConfigurationsMonthlyCycleModel


class MonthlyCycleCreateHandler(CoreGenericBaseHandler):
    """
    Handler to manage creation of LoanConfigurationsMonthlyCycleModel instances.

    Responsibilities:
        - Validates input data (title uniqueness, valid status).
        - Creates a new Monthly Cycle record in an atomic transaction.
    """

    _activity_type: str = "CONFIGURATION_MONTHLY_CYCLE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):
        """
        Validates input data before creation.

        Checks:
            - Title must be unique (no duplicate allowed).
            - Status, if provided, must be either "ACTIVATED" or "DEACTIVATED".

        Returns:
            - Sets an error message via `self.set_error_message()` if validation fails.
        """

        if not self.data.get("title"):
            return self.set_error_message(
                MONTHLY_CYCLE_TITLE_REQUIRED_ERROR_MESSAGE, key="title"
            )

        # Check if a Monthly Cycle with the same title already exists
        if self.queryset.filter(title__iexact=self.data.get("title")).exists():
            return self.set_error_message(
                MONTHLY_CYCLE_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        self.context["logger"].info("Validating Monthly Cycle Create Handler")

    def create(self):
        """
        Creates a new Monthly Cycle record using validated input data.

        Uses a Django atomic transaction to ensure data consistency.

        Fields expected in `self.data`:
            - title: Required
            - (optional) status: Not saved currently, but may be handled later
        """
        with transaction.atomic():
            # Create a new instance of the Monthly Cycle
            instance: LoanConfigurationsMonthlyCycleModel = self.queryset.create(
                title=self.data.get("title"),
                description=self.data.get("description"),
                # Note: status is not saved here — you may add it if needed
            )
            self.update_core_generic_created_by(instance=instance)

            self.context["logger"].info(
                f"Monthly Cycle created successfully. Monthly Cycle ID : {instance.pk}"
            )
