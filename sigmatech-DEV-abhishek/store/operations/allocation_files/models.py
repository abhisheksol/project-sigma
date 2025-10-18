from django.db import models
import uuid
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.models import (
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProductAssignmentModel,
)
from store.operations.allocation_files.v1.utils.enums import AllocationStatusEnum


class AllocationFileModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="ALLOCATION_FILE_ID",
        editable=False,
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        db_column="ALLOCATION_FILE_NAME",
    )
    file_url = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        db_column="FILE_URL",
    )
    initial_file_url = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        db_column="INITIAL_FILE_URL",
    )
    latest_reupload_file_url = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        db_column="LATEST_REUPLOAD_FILE_URL",
    )
    latest_error_file_url = models.URLField(
        max_length=512,
        null=True,
        blank=True,
        db_column="LATEST_ERROR_FILE_URL",
    )
    cycle = models.ForeignKey(
        LoanConfigurationsMonthlyCycleModel,
        on_delete=models.CASCADE,
        related_name="AllocationFileModel_cycle",
        db_column="CYCLE_ID",
        null=True,
        blank=True,
    )
    product_assignment = models.ForeignKey(
        LoanConfigurationsProductAssignmentModel,
        on_delete=models.CASCADE,
        related_name="AllocationFileModel_product_assignment",
        db_column="PROCESS_PRODUCT_ASSIGNMENT_ID",
    )
    no_of_total_records = models.IntegerField(
        default=0,
        db_column="NO_OF_TOTAL_RECORDS",
    )
    no_of_valid_records = models.IntegerField(
        default=0,
        db_column="NO_OF_VALID_RECORDS",
    )
    no_of_error_records = models.IntegerField(
        default=0,
        db_column="NO_OF_ERROR_RECORDS",
    )
    no_of_duplicate_records = models.IntegerField(
        default=0,
        db_column="NO_OF_DUPLICATE_RECORDS",
    )
    expiry_date = models.DateTimeField(
        null=True,
        blank=True,
        db_column="ALLOCATION_FILE_EXPIRY_DATE",
    )
    allocation_status = models.CharField(
        max_length=20,
        db_column="ALLOCATION_FILE_STATUS",
        blank=True,
        default=AllocationStatusEnum.INPROCESS.value,
        choices=AllocationStatusEnum.choices(),
    )

    class Meta:
        db_table = "ALLOCATION_FILE_TABLE"
