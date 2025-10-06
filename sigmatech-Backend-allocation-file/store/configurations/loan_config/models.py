from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid


class LoanConfigurationsProcessModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BANK_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="BANK_NAME",
    )
    logo = models.URLField(
        null=True,
        blank=True,
        db_column="BANK_LOGO",
    )

    contact_person_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="CONTACT_PERSON_NAME"
    )
    contact_person_email = models.CharField(
        max_length=100, null=True, blank=True, db_column="CONTACT_PERSON_EMAIL"
    )
    contact_person_phone_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column="CONTACT_PERSON_PHONE_NUMBER",
    )

    class Meta:
        db_table = "BANK_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_process_title"),
        ]
        verbose_name = "Process"
        verbose_name_plural = "Processs"


class LoanConfigurationsProductsModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="PRODUCT_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="PRODUCT_NAME",
    )

    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="PRODUCT_DESCRIPTION"
    )

    class Meta:
        db_table = "PRODUCT_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_product_title"),
        ]


class LoanConfigurationsMonthlyCycleModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="CYCLE_ID",
        default=uuid.uuid4,
    )
    title = models.IntegerField(
        unique=True,
        db_column="CYCLE_NAME",
    )

    # added description field
    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="CYCLE_DESCRIPTION"
    )

    class Meta:
        db_table = "MONTHLY_CYCLE_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_cycle_title"),
        ]


class BucketRangeModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_column="BUCKET_RANGE_ID",
    )
    label = models.CharField(
        max_length=50,
        db_column="BUCKET_RANGE_LABEL",
    )
    # value = models.PositiveIntegerField(db_column="BUCKET_RANGE_VALUE")

    # value as string not int
    value = models.CharField(
        max_length=50,
        db_column="BUCKET_RANGE_VALUE",
    )

    class Meta:
        db_table = "BUCKET_RANGE_TABLE"
        indexes = [
            models.Index(fields=["label"], name="idx_bucket_range_label"),
        ]


class LoanConfigurationsBucketModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BUCKET_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="BUCKET_NAME",
    )
    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="BUCKET_DESCRIPTION"
    )

    range = models.ForeignKey(
        BucketRangeModel,
        on_delete=models.CASCADE,
        null=True,
        db_column="BUCKET_RANGE_ID",
        related_name="LoanConfigurationsBucketModel_range",
    )

    class Meta:
        db_table = "BUCKET_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_bucket_title"),
        ]


class LoanConfigurationsProductAssignmentModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BANK_PRODUCT_ASSIGNMENT_ID",
        default=uuid.uuid4,
    )
    process = models.ForeignKey(
        LoanConfigurationsProcessModel,
        on_delete=models.CASCADE,
        related_name="LoanConfigurationsProductAssignmentModel_process",
        db_column="BANK_ID",
    )
    product = models.ForeignKey(
        LoanConfigurationsProductsModel,
        on_delete=models.CASCADE,
        related_name="LoanConfigurationsProductAssignmentModel_product",
        db_column="PRODUCT_ID",
    )
    min_due_percentage = models.FloatField(
        null=True,
        blank=True,
        db_column="MIN_DUE_PERCENTAGE",
    )
    refer_back_percentage = models.FloatField(
        null=True,
        blank=True,
        db_column="REFER_BACK_PERCENTAGE",
    )

    class Meta:
        db_table = "BANK_PRODUCT_ASSIGNMENT_TABLE"
        indexes = [
            models.Index(fields=["process"]),
            models.Index(fields=["product"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["process", "product"], name="UNIQUE_BANK_PRODUCT"
            ),
        ]
