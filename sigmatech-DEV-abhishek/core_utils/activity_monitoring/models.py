import uuid
from django.db import models
from core_utils.activity_monitoring.enums import (
    ActivityMonitoringBackGroundActivityEnum,
    ActivityMonitoringBackGroundStatusEnum,
    ActivityMonitoringMethodTypeEnumChoices,
)
from core_utils.utils.generics.generic_models import CoreGenericModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

# Create your models here.


class ActivityMonitoringLinkedEntityModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="ACTIVITY_LINKED_ENITY_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100, unique=True, db_column="ACTIVITY_LINKED_ENITY_TITLE"
    )

    class Meta:
        db_table = "ACTIVITY_LINKED_ENITY_TABLE"

    def __str__(self):
        return self.title


class ActivityTypeModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="ACTIVITY_TYPE_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(max_length=100, unique=True, db_column="ACTIVITY_TYPE")
    lable = models.CharField(max_length=255, db_column="ACTIVITY_TITLE", null=True)
    linked_entity = models.ForeignKey(
        ActivityMonitoringLinkedEntityModel,
        on_delete=models.CASCADE,
        related_name="ActivityMonitoringLogModel_linked_entity",
        null=True,
    )

    class Meta:
        db_table = "ACTIVITY_TYPE_TABLE"

    def __str__(self):
        return self.title


class ActivityMonitoringMethodTypeColorPreferenceModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="ACTIVITY_METHOD_COLOR_PREFERENCE_ID",
        default=uuid.uuid4,
    )
    method = models.CharField(
        max_length=50,
        choices=ActivityMonitoringMethodTypeEnumChoices.choices(),
        unique=True,
        db_column="METHOD",
    )
    color = models.CharField(max_length=100, db_column="COLOR")

    class Meta:
        db_table = "ACTIVITY_METHOD_COLOR_PREFERENCE_TABLE"


class ActivityMonitoringLogModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="ACTIVITY_MONITORING_LOG_ID",
        default=uuid.uuid4,
    )
    model_instance = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="ActivityMonitoringLogModel_model",
        db_column="MODEL_INSTANCE",
        null=True,
        blank=True,
    )
    primary_key = models.CharField(
        max_length=100, db_column="PRIMARY_KEY", null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True, db_column="ACTIVITY_LOG_DESCRIPTION"
    )

    activity_type = models.ForeignKey(
        ActivityTypeModel,
        on_delete=models.CASCADE,
        related_name="ActivityMonitoringLogModel_activity_type",
        db_column="ACTIVITY_TYPE_ID",
        null=True,
        blank=True,
    )
    performed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="ActivityMonitoringLogModel_performed_by",
    )
    method = models.ForeignKey(
        ActivityMonitoringMethodTypeColorPreferenceModel,
        on_delete=models.CASCADE,
        related_name="ActivityMonitoringLogModel_method",
        db_column="METHOD_ID",
    )

    old_data = models.JSONField(blank=True, null=True, db_column="OLD_DATA")
    new_data = models.JSONField(blank=True, null=True, db_column="NEW_DATA")

    class Meta:
        db_table = "ACTIVITY_MONITORING_LOG_TABLE"
        ordering = ("-core_generic_created_at",)


class ActivityMonitoringBackGroundActivityModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="ACTIVITY_MONITORING_LOG_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=32,
        choices=ActivityMonitoringBackGroundActivityEnum.choices(),
        db_column="BACK_GROUND_TASK_TYPE",
    )
    primary_key = models.CharField(
        max_length=100, db_column="PRIMARY_KEY", null=True, blank=True
    )
    end_time = models.DateTimeField(db_column="TASK_END_TIME", null=True, blank=True)
    status = models.CharField(
        max_length=32,
        choices=ActivityMonitoringBackGroundStatusEnum.choices(),
        blank=True,
        null=True,
    )
    percentage = models.FloatField(
        db_column="TASK_PROGESS_PERCENTAGE", blank=True, null=True
    )

    description = models.TextField(db_column="DESCRIPTION", null=True, blank=True)

    class Meta:
        db_table = "ACTIVITY_MONITORING_BACK_GROUND_TASK_TABLE"
