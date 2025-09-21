from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from typing import Optional, Dict
from store.configurations.loan_config.models import (
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProductAssignmentModel,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplatePreferenceModel,
)
from store.operations.allocation_files.v1.generics.utils.validations.allocation_file_payload_validation import (
    UploadAllocationFilePayloadValidation,
)


class UploadAllocationFileHandler(
    CoreGenericBaseHandler, UploadAllocationFilePayloadValidation
):
    """
    file_url : Url
    file_name : string
    cycle_id : UUID
    product_id : UUID
    process_id : UUID
    """

    cycle_instance: LoanConfigurationsMonthlyCycleModel
    product_assignment_instance: LoanConfigurationsProductAssignmentModel
    template_instance: ProcessTemplatePreferenceModel

    def validate(self):
        # ? check if any validation error exist in payload
        payload_error_message: Optional[Dict[str, str]] = self.is_valid()
        if payload_error_message:
            return self.set_error_message(**payload_error_message)

    def create(self):
        return
