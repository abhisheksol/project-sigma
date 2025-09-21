from django.db import models
from django.contrib.auth import get_user_model
from core_utils.utils.generics.generic_models import CoreGenericModel


# Create your models here.
class NotificationTypeModel(CoreGenericModel):
    id = models.BigAutoField(
        primary_key=True, unique=True, editable=False, db_column="ID"
    )
    title = models.CharField(max_length=100, null=True, blank=True, db_column="TITLE")
    description = models.TextField(null=True, blank=True, db_column="DESCRIPTION")
    is_active = models.BooleanField(
        default=True,
        db_column="IS_ACTIVE",
    )

    class Meta:
        ordering = ("-core_generic_created_at",)
        db_table = "NOTIFICATION_TYPE_TABLE"


class NotificationModel(CoreGenericModel):
    id = models.BigAutoField(
        primary_key=True, unique=True, editable=False, db_column="ID"
    )
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="NotificationModel_user",
        db_column="USER_ID",
    )
    notification_type = models.ForeignKey(
        NotificationTypeModel,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
        db_column="NOTIFICATION_TYPE",
    )
    title = models.CharField(max_length=500, null=True, blank=True, db_column="TITLE")
    message = models.TextField(null=True, blank=True, db_column="MESSAGE")
    is_read = models.BooleanField(default=False, db_column="IS_READ")
    read_at = models.DateTimeField(null=True, blank=True, db_column="READ_AT")
    is_cleared = models.BooleanField(default=False, db_column="IS_CLEARED")
    cleared_at = models.DateTimeField(null=True, blank=True, db_column="CLEARED_AT")
    is_mention = models.BooleanField(default=False, db_column="IS_MENTION")
    is_routing = models.BooleanField(default=False, db_column="IS_ROUTING")
    route_data = models.JSONField(null=True, blank=True, db_column="ROUTE_DATA")
    notification_icon = models.CharField(
        max_length=100, null=True, blank=True, db_column="ICON"
    )

    mentioned_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="NotificationModel_mentioned_user",
        db_column="MENTIONED_BY",
    )
    is_deleted = models.BooleanField(default=False, db_column="IS_DELETED")

    class Meta:
        ordering = ("-core_generic_created_at",)
        db_table = "NOTIFICATION_TABLE"
