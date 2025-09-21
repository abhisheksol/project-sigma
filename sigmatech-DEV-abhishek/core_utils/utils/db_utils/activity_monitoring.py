from django.contrib.auth.models import AbstractBaseUser
from typing import Optional, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

from core_utils.activity_monitoring.models import (
    ActivityMonitoringLogModel,
    ActivityMonitoringMethodTypeColorPreferenceModel,
    ActivityTypeModel,
)
from core_utils.utils.enums import status_list_enum_values
from core_utils.utils.santize_data import object_to_json
import logging
from core.settings import logger


class ActivityMonitoringLogger:
    """
    Utility class to log activity monitoring events into
    `ActivityMonitoringLogModel`.

    This class encapsulates:
        - The model instance being acted on
        - Activity type (from `ActivityTypeModel`)
        - The user who performed the action
        - The method (from `ActivityMonitoringMethodTypeColorPreferenceModel`)
        - Old and new serialized data of the model instance

    Typical usage:
        logger = ActivityMonitoringLogger()
        logger.set_model_instance(instance)
        logger.set_activity_type("User Created")
        logger.set_performed_by(user)
        logger.set_method("POST")
        logger.set_old_data(old_instance)
        logger.set_new_data(new_instance)
        logger.activity_monitoring_log()
    """

    # Queryset used for creating activity log entries
    activity_monitoring_log_queryset: QuerySet[ActivityMonitoringLogModel] = (
        ActivityMonitoringLogModel.objects.all()
    )

    # Internal tracking fields
    _model_instance: Optional[models.Model] = None
    _primary_key: Optional[str] = None
    _activity_type: Optional[str] = None
    _performed_by: Optional[models.Model] = None
    _method: Optional[ActivityMonitoringMethodTypeColorPreferenceModel] = None
    _old_data: Optional[dict] = None
    _new_data: Optional[dict] = None

    logger: logging.LoggerAdapter = logging.LoggerAdapter(
        logger, {"app_name": "ActivityMonitoringLogger"}
    )

    # ---------- Setters / Getters ----------

    def set_model_instance(self, instance: models.Model) -> None:
        """
        Store the model instance and capture its primary key.
        """
        self._model_instance = instance
        self._primary_key = str(instance.pk)

    def get_model_instance(self) -> Optional[models.Model]:
        return self._model_instance

    def set_activity_type(self, activity_type: str) -> None:
        """
        Store the activity type name.

        This will be resolved into an `ActivityTypeModel` before saving.
        """
        self._activity_type = activity_type

    def get_activity_type(self) -> Optional[str]:
        return self._activity_type

    def set_performed_by(self, user: models.Model) -> None:
        """
        Store the user who performed the action.
        """
        self._performed_by = user

    def get_performed_by(self) -> Optional[models.Model]:
        return self._performed_by

    def set_method(self, method: str) -> None:
        """
        Resolve and store the method as an
        `ActivityMonitoringMethodTypeColorPreferenceModel`.

        Args:
            method (str): Method string (e.g., 'POST', 'PUT', 'DELETE').
        """
        if isinstance(self._method, ActivityMonitoringMethodTypeColorPreferenceModel):
            return
        self._method: ActivityMonitoringMethodTypeColorPreferenceModel = (
            ActivityMonitoringMethodTypeColorPreferenceModel.objects.get(method=method)
        )

    def get_method(self) -> ActivityMonitoringMethodTypeColorPreferenceModel:
        """
        Retrieve the stored method model.
        """
        return self._method

    def set_old_data(self, instance: Optional[models.Model]) -> None:
        """
        Store serialized data of the model before update.
        """
        self._old_data = object_to_json(instance) if instance else None

    def get_old_data(self) -> Optional[dict]:
        return self._old_data

    def set_new_data(self, instance: Optional[models.Model]) -> None:
        """
        Store serialized data of the model after update.
        """
        self._new_data = object_to_json(instance) if instance else None

    def get_new_data(self) -> Optional[dict]:
        return self._new_data

    def get_activity_type_model(self) -> ActivityTypeModel:
        """
        Resolve and return the `ActivityTypeModel` instance.

        Raises:
            ValueError: If activity type is not set.
        """
        if not self._activity_type:
            raise ValueError("Activity type not set.")
        return ActivityTypeModel.objects.get(title=self._activity_type)

    # ---------- Logging Methods ----------

    def activity_monitoring_log(self) -> ActivityMonitoringLogModel:
        """
        Create a single activity monitoring log entry.

        Returns:
            ActivityMonitoringLogModel: The created log record.

        Raises:
            ValueError: If model instance is missing.
        """
        if not self._model_instance:
            raise ValueError("Model instance must be set before logging.")

        content_type = ContentType.objects.get_for_model(
            self._model_instance, for_concrete_model=False
        )
        activity_log_instance: ActivityMonitoringLogModel = (
            self.activity_monitoring_log_queryset.create(
                model_instance=content_type,
                primary_key=self._primary_key,
                activity_type=self.get_activity_type_model(),
                performed_by=self._performed_by,
                method=self.get_method(),
                old_data=self._old_data,
                new_data=self._new_data,
            )
        )

        self.logger.info(
            f"Activity '{activity_log_instance.activity_type.title}' "
            f"'{activity_log_instance.method}' logged successfully. "
            f"ID: {activity_log_instance.pk}"
        )
        return activity_log_instance

    def activity_monitoring_log_bulk_instances(self) -> ActivityMonitoringLogModel:
        """
        Create an activity log entry for bulk operations.

        Note:
            This does not attach specific model instances or old/new data.
        """
        activity_log_instance: ActivityMonitoringLogModel = (
            self.activity_monitoring_log_queryset.create(
                activity_type=self.get_activity_type_model(),
                performed_by=self.request.user,
                method=self._method,
            )
        )

        self.logger.info(
            f"Bulk Activity '{activity_log_instance.activity_type.title}' "
            f"'{activity_log_instance.method}' logged successfully. "
            f"ID: {activity_log_instance.pk}"
        )
        return activity_log_instance

    # ---------- Helpers for Status Update Validation ----------

    def is_status_update_method(self) -> bool:
        """
        Check if payload corresponds to a status update operation.

        Expected payload structure:
            {
                "id": "<uuid>",
                "status": "<status-value>"
            }

        Returns:
            bool: True if payload is a valid status update candidate.
        """
        payload_data: Dict = self.data
        return (
            len(payload_data.keys()) == 2
            and "id" in payload_data
            and "status" in payload_data
        )

    def valid_status_enum(self) -> bool:
        """
        Validate if payload `status` belongs to the allowed enum values.

        Returns:
            bool: True if status is valid, False otherwise.
        """
        if not self.is_status_update_method():
            return False
        return self.data["status"] in status_list_enum_values()


def activity_monitoring_logger(
    instance: models.Model,
    user: AbstractBaseUser,
    method: str,
    activity_type: str,
    old_instance: Optional[models.Model] = None,
    new_instance: Optional[models.Model] = None,
) -> ActivityMonitoringLogModel:
    """
    Utility function to quickly log an activity without
    explicitly instantiating the logger class.

    Args:
        instance (models.Model): Target model instance.
        user (AbstractBaseUser): User performing the action.
        method (str): HTTP method (e.g., 'POST', 'PUT', 'DELETE').
        activity_type (str): Activity type title (linked to `ActivityTypeModel`).
        old_instance (Optional[models.Model]): State before update.
        new_instance (Optional[models.Model]): State after update.

    Returns:
        ActivityMonitoringLogModel: The created activity log entry.
    """
    logger = ActivityMonitoringLogger()
    logger.set_model_instance(instance)
    logger.set_performed_by(user)
    logger.set_method(method)
    logger.set_activity_type(activity_type)
    logger.set_old_data(old_instance)
    logger.set_new_data(new_instance)

    return logger.activity_monitoring_log()
