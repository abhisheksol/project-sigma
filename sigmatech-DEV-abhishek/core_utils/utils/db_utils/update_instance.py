from django.db import models
from typing import Optional

from core_utils.activity_monitoring.models import ActivityMonitoringLogModel
from core_utils.utils.db_utils.activity_monitoring import ActivityMonitoringLogger


class CoreGenericCrudHandlerUtils(ActivityMonitoringLogger):
    """
    Utility class for CRUD operations with integrated activity monitoring.

    Inherits from `ActivityMonitoringLogger` to handle automatic activity logs
    whenever model instances are created, updated, or modified.

    Expected:
        - `self.request.user` is available (e.g., within Django Views or Serializers).
        - `self.activity_type` and `self.method` should be set before logging.
        - Handles toast notification values to show user-friendly feedback.
    """

    # Default key used for extracting toast notification values from model instances
    key: str = "title"

    # Optional manual override for toast notification value
    toast_value: Optional[str] = None

    # -------------------------------
    # Toast Notification Utilities
    # -------------------------------

    def get_toast_message_value(self, instance: models.Model) -> str:
        """
        Determines the value to display in toast notifications.

        Priority:
            1. Use manually set `self.toast_value` (if provided).
            2. Use the attribute defined by `self.key` from the model instance.

        Args:
            instance (models.Model): The model instance being processed.

        Returns:
            str: The resolved toast message value.

        Raises:
            Exception: If neither `toast_value` nor the `key` attribute exists.
        """
        if not hasattr(self, "data"):
            self.data = {}

        if self.toast_value:
            self.data["toast_message_value"] = self.toast_value
        elif self.key and hasattr(instance, self.key):
            self.data["toast_message_value"] = getattr(instance, self.key)
        else:
            raise Exception("Invalid key to return toast message value")

        return self.data["toast_message_value"]

    def set_toast_message_value(self, value: str) -> None:
        """
        Explicitly set a manual value for toast notifications.

        Args:
            value (str): Custom toast message value.
        """
        self.toast_value = value

    # -------------------------------
    # CRUD + Logging Utilities
    # -------------------------------

    def update_core_generic_updated_by(
        self, instance: models.Model, log_activity: bool = False
    ) -> None:
        """
        Updates the `core_generic_updated_by` field of the instance
        and prepares new data for logging.

        Args:
            instance (models.Model): The model instance being updated.
        """
        if self.request.user.is_authenticated:
            instance.core_generic_updated_by = self.request.user.UserDetailModel_user

        # Prepare log "new_data" snapshot
        self.get_toast_message_value(instance=instance)
        self.set_new_data(instance)
        if log_activity:
            # Create and persist activity log
            if self.request.user.is_authenticated:
                instance.core_generic_created_by = (
                    self.request.user.UserDetailModel_user
                )
                instance.save()

            # Prepare logger fields for creation
            self.set_model_instance(instance)
            self.set_performed_by(self.request.user)
            self.set_new_data(instance)
            self.set_method(self._method)
            # Create and persist activity log
            activity_log_instance: ActivityMonitoringLogModel = (
                self.activity_monitoring_log()
            )
            self.set_activity_log_instance(activity_log_instance=activity_log_instance)
            # Set toast message
            if not self.toast_value:
                self.get_toast_message_value(instance=instance)
            print("self.toast_value", self.toast_value)

    def update_core_generic_created_by(self, instance: models.Model) -> None:
        """
        Updates the `core_generic_created_by` field and logs the creation action.

        Args:
            instance (models.Model): The newly created model instance.
        """
        if self.request.user.is_authenticated:
            instance.core_generic_created_by = self.request.user.UserDetailModel_user
            instance.save()

        # Prepare logger fields for creation
        self.set_model_instance(instance)
        self.set_performed_by(self.request.user)
        self.set_new_data(instance)
        self.set_method(self._method)
        # Create and persist activity log
        activity_log_instance: ActivityMonitoringLogModel = (
            self.activity_monitoring_log()
        )
        self.set_activity_log_instance(activity_log_instance=activity_log_instance)
        # Set toast message
        self.get_toast_message_value(instance=instance)

    def update_model_instance(self, instance: models.Model, data: dict) -> models.Model:
        """
        Updates a model instance with provided data, logs the change,
        and returns the updated instance.

        Workflow:
            1. Store pre-update state (`old_data`).
            2. Apply updates and save.
            3. Store post-update state (`new_data`).
            4. Persist activity log.

        Args:
            instance (models.Model): The model instance to update.
            data (dict): Dictionary of field updates.

        Returns:
            models.Model: The updated model instance.
        """
        # Store pre-update state for logging
        self.set_old_data(instance)

        # Apply updates
        for key, value in data.items():
            setattr(instance, key, value)
        self.update_core_generic_updated_by(instance=instance)
        instance.save()

        # Store post-update state
        self.set_model_instance(instance)
        self.set_performed_by(self.request.user)
        self.set_new_data(instance)
        self.set_method(self._method)

        # Persist activity log
        activity_log_instance: ActivityMonitoringLogModel = (
            self.activity_monitoring_log()
        )
        self.set_activity_log_instance(activity_log_instance=activity_log_instance)

        return instance

    # -------------------------------
    # Activity Log Helpers
    # -------------------------------

    def set_activity_log_instance(
        self, activity_log_instance: ActivityMonitoringLogModel
    ) -> None:
        """
        Stores the created `ActivityMonitoringLogModel` instance in `self.data`.

        Args:
            activity_log_instance (ActivityMonitoringLogModel): The created activity log entry.
        """
        self.data["activity_log_instance"] = activity_log_instance

    def set_activity_monitoring_log_bulk_instances(
        self, toast_message_value: Optional[str]
    ) -> None:
        """
        Handles bulk creation of activity monitoring logs.

        Args:
            toast_message_value (Optional[str]): Custom toast message value for the bulk operation.
        """

        if self.toast_value:
            self.set_toast_message_value(toast_message_value)
        if isinstance(self._method, str):
            self.set_method(method=self._method)
        self.activity_monitoring_log_bulk_instances()
