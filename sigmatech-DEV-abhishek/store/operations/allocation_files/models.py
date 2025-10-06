import datetime
import re
import logging
from django.db import models
from django.utils import timezone
import uuid
from core_utils.utils.generics.generic_models import CoreGenericModel
from store.configurations.loan_config.models import (
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProductAssignmentModel,
)

logger = logging.getLogger(__name__)


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
        Compute expiry_date based on core_generic_created_at and cycle information.

        - Attempts to parse number of days from cycle.title (first integer found).
        - If that fails, tries common numeric attrs on the cycle instance.
        - If still not found, falls back to a safe default (30 days).
        - Uses core_generic_created_at if available, otherwise timezone.now().
        - Does not raise on unparsable cycle.title to avoid admin errors.
        """
        if not self.expiry_date:
            cycle_days = None
            cycle_obj = getattr(self, "cycle", None)

            # 1) try extracting integer from cycle.title (e.g. "Cycle 10" or "10")
            if cycle_obj is not None:
                title = getattr(cycle_obj, "title", None)
                if title is not None:
                    m = re.search(r"(\d+)", str(title))
                    if m:
                        try:
                            cycle_days = int(m.group(1))
                        except (ValueError, TypeError):
                            cycle_days = None

            # 2) try common numeric attributes on cycle model
            if cycle_days is None and cycle_obj is not None:
                for attr in ("days", "duration", "num_days", "day"):
                    val = getattr(cycle_obj, attr, None)
                    if val is None:
                        continue
                    try:
                        cycle_days = int(val)
                        break
                    except (ValueError, TypeError):
                        continue

            # 3) Validate parsed value; allow 1-31 or 99 as special (indefinite)
            if cycle_days is not None:
                if not (1 <= cycle_days <= 31 or cycle_days == 99):
                    logger.warning(
                        "Parsed cycle_days=%r is out of expected range; falling back to default",
                        cycle_days,
                    )
                    cycle_days = None

            # 4) base date and fallback default
            base_date = getattr(self, "core_generic_created_at", None) or timezone.now()
            if cycle_days is None:
                # choose a safe default so admin creation doesn't fail
                cycle_days = 30
                logger.info(
                    "Could not determine cycle days from %r; defaulting to %d days",
                    getattr(cycle_obj, "title", None),
                    cycle_days,
                )

            # 5) set expiry_date (if cycle_days == 99 treat as far future date)
            if cycle_days == 99:
                # set a far future expiry (e.g., 100 years)
                self.expiry_date = base_date + datetime.timedelta(days=365 * 100)
            else:
                self.expiry_date = base_date + datetime.timedelta(days=cycle_days)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "ALLOCATION_FILE_TABLE"