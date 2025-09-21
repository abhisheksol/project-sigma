from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.loan_config.api.v1.utils.constants import (
    ENSUSRE_CONTACT_PERSON_PHONE_NUMBER,
    PROCESS_TITLE_ALREADY_EXISTS_ERROR_MESSAGE,
    PROCESS_TITLE_REQUIRED_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import LoanConfigurationsProcessModel
from django.db import transaction
from typing import Union


class ProcessCreateHandler(CoreGenericBaseHandler):
    """
    Handler for creating a new Loan Configurations Process.

    Inherits from:
        CoreGenericBaseHandler – Provides base error handling and response utilities.

    Responsibilities:
        - Validates input data before creation.
        - Ensures uniqueness of title and code.
        - Checks enum value of status.
        - Creates the LoanConfigurationsProcessModel instance inside an atomic transaction.
    """

    _activity_type: str = "CONFIGURATION_PROCESS_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):
        print("================>")
        """
        Validates the incoming data for creating a LoanConfigurationsProcessModel.

        Checks:
            - Title and code are provided.
            - Title and code are unique in the queryset.
            - Status is either 'ACTIVATED' or 'DEACTIVATED'.

        Returns:
            Sets error messages using `set_error_message` if validation fails.
        """
        title: Union[str, None] = self.data.get("title")
        contact_person_phone_number: Union[str, None] = str(
            self.data.get("contact_person_phone_number", "")
        )

        if not title:
            return self.set_error_message(
                PROCESS_TITLE_REQUIRED_ERROR_MESSAGE, key="title"
            )

        if self.queryset.filter(title__iexact=title).exists():
            return self.set_error_message(
                PROCESS_TITLE_ALREADY_EXISTS_ERROR_MESSAGE, key="title"
            )

        if contact_person_phone_number and len(contact_person_phone_number) != 10:
            return self.set_error_message(
                ENSUSRE_CONTACT_PERSON_PHONE_NUMBER, key="contact_person_phone_number"
            )

    def create(self):
        """
        Creates a new LoanConfigurationsProcessModel record.

        Performs the creation inside a Django atomic transaction block for data safety.

        Fields expected in `self.data`:
            - title
            - code
            - logo
            - status (default: 'ACTIVATED')
            - contact_person_name
            - contact_person_email
            - contact_person_phone_number

        Logs the success message along with the newly created instance's ID.
        """
        with transaction.atomic():
            instance: LoanConfigurationsProcessModel = self.queryset.create(**self.data)
            self.update_core_generic_created_by(instance=instance)

            self.context["logger"].info(
                f"Process created successfully. Process ID : {instance.pk}"
            )
