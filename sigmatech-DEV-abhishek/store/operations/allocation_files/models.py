import datetime
from django.db import models
import uuid
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.models import (
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProductAssignmentModel,
)


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

    def save(self, *args, **kwargs) -> None:
        """
        Override the save method to compute the expiry_date based on core_generic_created_at
        and cycle.title.

        Assumes cycle.title is a string or integer representing the number of days.
        If cycle.title is not a valid integer, raises a ValueError.
        """
        if not self.expiry_date:
            try:
                # Convert cycle.title to an integer
                cycle_days = int(self.cycle.title)
                # Calculate expiry_date based on core_generic_created_at and cycle.title
                self.expiry_date = self.core_generic_created_at + datetime.timedelta(
                    days=cycle_days
                )
            except (ValueError, TypeError):
                raise ValueError(
                    "cycle.title must be a valid integer representing days"
                )

        super().save(*args, **kwargs)

    class Meta:
        db_table = "ALLOCATION_FILE_TABLE"
        # indexes = [
        #     models.Index(fields=["cycle"], name="idx_alloc_cycle"),
        #     models.Index(
        #         fields=["product_assignment"], name="idx_alloc_product_assignment"
        #     ),
        #     models.Index(fields=["expiry_date"], name="idx_alloc_expiry_date"),
        # ]
