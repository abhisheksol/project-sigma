from core_utils.utils.generics.generic_models import CoreGenericModel
from django.db import models
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
import uuid

from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
    CustomAllocationMultiReferenceFieldValueTypeEnum,
    DateFormatEnum,
    DateTimeFormatEnum,
    DurationFormatEnum,
    SQLDataTypeEnum,
    CustomAllocatinFileTemplateStatusEnum,
    CustomAllocatinFileTemplateFieldStatusEnum,
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


class SQLDataTypeModel(models.Model):
    """
    Table for supported SQL field data types + formatting rules.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="DATA_TYPE_ID",
    )
    title = models.CharField(
        max_length=128,
        unique=True,
        choices=SQLDataTypeEnum.choices(),
        db_column="DATA_TYPE_TITLE",
    )

    class Meta:
        db_table = "SQL_DATA_TYPE_TABLE"
        verbose_name = "SQL Data Type"
        verbose_name_plural = "SQL Data Types"

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
    data_type = models.ForeignKey(
        SQLDataTypeModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="DATA_TYPE_ID",
        related_name="field_mappings",
    )
    is_required_field = models.BooleanField(default=True, db_column="IS_REQUIRED_FIELD")
    ordering = models.IntegerField(default=0, db_column="EXCEL_HEADER_ORDER")
    preference_name = models.CharField(
        max_length=512, db_column="PREFERENCE_NAME", blank=True, null=True
    )
    is_multi_ref_field = models.BooleanField(
        default=False, db_column="IS_MULTI_REFERENCE_FIELD"
    )
    value_type = models.CharField(
        max_length=128,
        choices=CustomAllocationMultiReferenceFieldValueTypeEnum.choices(),
        null=True,
        blank=True,
        db_column="VALUE_TYPE",
    )

    status = models.CharField(
        max_length=128,
        choices=CustomAllocatinFileTemplateFieldStatusEnum.choices(),
        default=CustomAllocatinFileTemplateFieldStatusEnum.MAPPED.value,
        db_column="TEMPLATE_FIELD_STATUS",
    )
    auto_fill_errors = models.TextField(
        blank=True,
        null=True,
        db_column="AUTO_FILL_ERRORS",
    )
    # Optional format rules (single choice)
    date_format = models.CharField(
        max_length=32,
        choices=DateFormatEnum.choices(),
        null=True,
        blank=True,
        db_column="SUPPORTED_DATE_FORMAT",
    )
    datetime_format = models.CharField(
        max_length=64,
        choices=DateTimeFormatEnum.choices(),
        null=True,
        blank=True,
        db_column="SUPPORTED_DATETIME_FORMAT",
    )
    duration_format = models.CharField(
        max_length=64,
        choices=DurationFormatEnum.choices(),
        null=True,
        blank=True,
        db_column="SUPPORTED_DURATION_FORMAT",
    )

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
