from django.db.models.query import QuerySet
from django.db.models import Model
from typing import Dict, Union, List, Optional, Any
from rest_framework.response import Response
from rest_framework import status
from core.settings import logger
import logging
import inspect

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.activity_monitoring.models import (
    ActivityMonitoringLogModel,
    ActivityMonitoringMethodTypeColorPreferenceModel,
)
from core_utils.utils.enums import CoreUtilsStatusEnum


class CoreGenericUtils:
    """
    A utility mixin class providing common helper methods for:
        - Logging
        - Activity monitoring integration
        - Toast (user feedback) handling
        - Queryset and request parameter access
        - Standardized success/error responses

    Typically used in DRF Views, Handlers, or Serializers
    that need consistent response and logging behavior.
    """

    # -------------------------------
    # Class attributes
    # -------------------------------

    toast_message_value: str = ""  # Custom value for user feedback
    activity_log_instance: Optional[ActivityMonitoringLogModel] = None
    queryset: QuerySet  # Must be set in a subclass or dynamically

    # Default success messages based on HTTP method
    success_message: Dict[str, str] = {
        "POST": "Successfully created",
        "PUT": "Successfully updated",
        "DELETE": "Successfully deleted",
    }

    # Default exception fallback message
    exception_message: str = "Internal Server Error"

    # -------------------------------
    # Logging Utilities
    # -------------------------------

    def get_logger(self) -> logging.LoggerAdapter:
        """
        Creates and returns a contextual logger adapter.

        Context includes:
            - Class name
            - File path of caller

        Returns:
            logging.LoggerAdapter: Configured logger adapter instance.
        """
        frame: inspect.FrameInfo = inspect.stack()[1]  # Caller frame
        module: Optional[object] = inspect.getmodule(frame[0])
        class_name: str = self.__class__.__name__
        file_path: str = (
            module.__file__ if module and hasattr(module, "__file__") else "unknown"
        )

        adapter: logging.LoggerAdapter = logging.LoggerAdapter(
            logger, {"app_name": f"{class_name} | {file_path}"}
        )
        return adapter

    # -------------------------------
    # Toast message utilities
    # -------------------------------

    def get_toast_message_value(self) -> str:
        """
        Get the current toast message value.

        Returns:
            str: The toast message value.
        """
        return self.toast_message_value

    def set_toast_message_value(self, value: str) -> None:
        """
        Set a custom toast message value.

        Args:
            value (str): Custom message string.
        """
        self.toast_message_value = value

    def add_toast_message_to_activity_log(
        self, success_message: str, status: Optional[str] = None
    ) -> None:
        """
        Adds a toast message into the activity log description.

        Args:
            success_message (str): The success message to save.
        """
        instance: ActivityMonitoringLogModel = self.get_activity_log_instance()
        if not instance:
            return
        instance.description = success_message
        if status and status == CoreUtilsStatusEnum.ACTIVATED.value:
            instance.method = (
                ActivityMonitoringMethodTypeColorPreferenceModel.objects.get(
                    method=ActivityMonitoringMethodTypeEnumChoices.ACTIVATED.value
                )
            )
        elif status and status == CoreUtilsStatusEnum.DEACTIVATED.value:
            instance.method = (
                ActivityMonitoringMethodTypeColorPreferenceModel.objects.get(
                    method=ActivityMonitoringMethodTypeEnumChoices.INACTIVATED.value
                )
            )
        instance.save()

    def set_dynamic_toast_message(self, validated_data: Dict) -> str:
        """
        Constructs and applies a dynamic toast message based on:
            - The current HTTP method (POST/PUT/DELETE)
            - The pre-set `toast_message_value` if available.

        Args:
            validated_data (Dict): The payload data (can contain an activity log).

        Returns:
            str: The final toast message used in the response.
        """
        success_message: str = self.get_success_message()

        payload: Dict[str, Any] = self.request.data

        status: str = ""
        if len(payload.keys()) == 2 and "status" in payload.keys():
            if payload["status"] == CoreUtilsStatusEnum.ACTIVATED.value:
                success_message: str = (
                    self.toast_message_value + " " + "activated successfully"
                )
                status: str = CoreUtilsStatusEnum.ACTIVATED.value
            if payload["status"] == CoreUtilsStatusEnum.DEACTIVATED.value:
                success_message: str = (
                    self.toast_message_value + " " + "inactivated successfully"
                )
                status: str = CoreUtilsStatusEnum.DEACTIVATED.value

        # Prefix toast message if it exists
        elif isinstance(success_message, str):
            success_message: str = self.toast_message_value + " " + success_message

        # Store message in activity log
        self.add_toast_message_to_activity_log(
            success_message=success_message, status=status
        )

        # Remove log instance from payload to avoid leaking it to clients
        if isinstance(validated_data, dict) and validated_data.get(
            "activity_log_instance"
        ):
            validated_data.pop("activity_log_instance")
        if isinstance(success_message, str):
            return success_message.strip().capitalize()
        return success_message

    # -------------------------------
    # Activity Log Utilities
    # -------------------------------

    def set_activity_log_instance(self, instance: ActivityMonitoringLogModel) -> None:
        """
        Stores the activity log instance for later usage.

        Args:
            instance (ActivityMonitoringLogModel): Activity log model instance.
        """
        self.activity_log_instance = instance

    def get_activity_log_instance(self) -> ActivityMonitoringLogModel:
        """
        Retrieves the current activity log instance.

        Returns:
            ActivityMonitoringLogModel: The stored log instance.
        """
        return self.activity_log_instance

    # -------------------------------
    # Request Utilities
    # -------------------------------

    def get_params(self) -> Dict:
        """
        Retrieves query parameters from the request object.

        Returns:
            Dict: A dictionary of query parameters.
        """
        try:
            params: dict = self.request.GET.dict()
        except Exception:
            params: dict = self.request.GET
        return params

    def get_queryset(self) -> QuerySet[Model]:
        """
        Returns the active queryset (default: `.all()`).

        Returns:
            QuerySet[Model]: A Django queryset.
        """
        return self.queryset.all()

    def get_success_message(self) -> Optional[Any]:
        """
        Returns the default success message for the current HTTP method.

        Returns:
            Optional[str]: A success message or None if not mapped.
        """
        return self.success_message.get(self.request.method)

    def set_context_data(self) -> Dict:
        """
        Constructs and returns contextual data.

        Returns:
            Dict: Context containing the request, logger, and view kwargs.
        """
        context: Dict = {
            "request": self.request,
            "logger": self.get_logger(),
            **self.kwargs,
        }
        return context

    # -------------------------------
    # Response Helpers
    # -------------------------------

    def custom_handle_exception(self, e: Exception) -> Response:
        """
        Handles exceptions consistently:
            - Logs details
            - Returns a standardized error response

        Args:
            e (Exception): The raised exception.

        Returns:
            Response: DRF Response with error payload and HTTP 400.
        """
        self.get_logger().info(
            f"{type(self).__name__} Method {self.request.method} API Exception, {str(e)}"
        )
        return Response(
            {"message": self.exception_message, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def validation_response(self, validated_data: Dict) -> Response:
        """
        Returns a standardized validation error response.

        Args:
            validated_data (Dict): Must include 'error_message'.

        Returns:
            Response: DRF Response with error message and optional field errors.
        """
        return Response(
            {
                "message": validated_data["error_message"],
                "field_errors": validated_data.get("field_errors"),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def success_response(self, validated_data: Union[List, Dict]) -> Response:
        """
        Returns a standardized success response with logging.

        Args:
            validated_data (Union[List, Dict]): Data payload to return.

        Returns:
            Response: DRF Response with a success message and results.
        """
        self.get_logger().info("validated_data" + str(validated_data))
        success_message: str = self.set_dynamic_toast_message(
            validated_data=validated_data
        )
        return Response({"message": success_message, "results": validated_data})
