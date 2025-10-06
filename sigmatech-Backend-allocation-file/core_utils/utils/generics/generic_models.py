from django.db import models

from core_utils.utils.enums import CoreUtilsStatusEnum


class CoreGenericModel(models.Model):
    """
    All models in the project should inherit from CoreGenericModel, an abstract base model that centralizes common fields and logic. This allows for global control over all models in the application.
    """

    status = models.CharField(
        max_length=20,
        default=CoreUtilsStatusEnum.ACTIVATED.value,
        db_column="STATUS",
        blank=True,
        choices=CoreUtilsStatusEnum.choices(),
    )
    core_generic_created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_column="CORE_GENERIC_CREATED_AT"
    )
    core_generic_updated_at = models.DateTimeField(
        auto_now=True, null=True, db_column="CORE_GENERIC_LAST_UPDATED_AT"
    )
    core_generic_created_by = models.ForeignKey(
        "accounts.UserDetailModel",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        db_column="CORE_GENERIC_CREATED_BY",
    )
    core_generic_updated_by = models.ForeignKey(
        "accounts.UserDetailModel",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        db_column="CORE_GENERIC_UPDATED_BY",
    )

    class Meta:
        abstract = True
