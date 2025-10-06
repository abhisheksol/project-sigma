from core_utils.utils.generics.generic_models import CoreGenericModel
from django.db import models
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
import uuid

from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
    CustomAllocatinFileTemplateStatusEnum,
)

# Create your models here.


class ProcessTemplatePreferenceModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="TEMPLATE_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        db_column="TEMPLATE_NAME",
    )
    product_assignment = models.ForeignKey(
        LoanConfigurationsProductAssignmentModel,
        on_delete=models.CASCADE,
        related_name="ProcessTemplatePreferenceModel_process",
        db_column="PROCESS_PRODUCT_ASSIGNMENT_ID",
    )
    uploaded_file = models.URLField(
        max_length=512,
        db_column="UPLOADED_FILE_FOR_GENERATION_URL",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=128,
        choices=CustomAllocatinFileTemplateStatusEnum.choices(),
        default=CustomAllocatinFileTemplateStatusEnum.DRAFT.value,
        db_column="TEMPLATE_STATUS",
    )
    is_default = models.BooleanField(default=True, db_column="IS_DEFAULT")

    class Meta:
        db_table = "PROCESS_PRODUCT_TEMPLATE_TABLE"
        unique_together = ("product_assignment", "is_default")

    def __str__(self):
        return self.title


class ProcessTemplateFieldMappingModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="TEMPLATE_MAPPING_ID",
        default=uuid.uuid4,
    )

    template = models.ForeignKey(
        ProcessTemplatePreferenceModel,
        on_delete=models.CASCADE,
        related_name="ProcessTemplateFieldMappingModel_template",
        db_column="TEMPLATE_ID",
    )
    title = models.CharField(
        max_length=512,
        choices=CustomAllocationFileTemplateReservedFieldsEnum.choices(),
        db_column="RESERVED_FIELD_NAME",
    )
    label = models.CharField(
        max_length=512, db_column="DISPLAY_NAME", blank=True, null=True
    )
    is_required_field = models.BooleanField(default=True, db_column="IS_REQUIRED_FIELD")

    class Meta:
        db_table = "TEMPLATE_FIELD_MAPPING_TABLE"
        unique_together = ("template", "title")
        # ? bucket possible fields should be validated from configuration

    def __str__(self):
        return self.title


class ProcessTemplateMultiReferenceFieldModel(CoreGenericModel):
    reference_field = models.ForeignKey(
        ProcessTemplateFieldMappingModel,
        on_delete=models.CASCADE,
        related_name="ProcessTemplateMultiReferenceFieldModel_reference_field",
        db_column="TEMPLATE_FIELD_MAPPING_ID",
    )
    title = models.CharField(
        max_length=512, db_column="MULTI_REFERENCE_CUSTOM_FIELD_NAME"
    )
    label = models.CharField(
        max_length=512, db_column="MULTI_REFERENCE_CUSTOM_FIELD_LABEL"
    )

    class Meta:
        db_table = "TEMPLATE_FIELD__TABLE"
