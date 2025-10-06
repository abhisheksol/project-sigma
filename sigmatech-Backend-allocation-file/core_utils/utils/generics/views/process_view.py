from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from typing import Dict
from core_utils.utils.constants import CORE_UTILS_DEV_ERROR_MESSAGE
from core_utils.utils.generics.views.core_generic_utils import CoreGenericUtils
from core_utils.utils.generics.views.queryset import CoreGenericQuerysetInstance


class CoreGenericProcessDataAPIView(CoreGenericUtils):
    """
    A base API view designed to handle data processing using DRF serializers.
    Supports data ingestion from various request types (JSON, multipart, query params),
    with validation, business logic execution, and standardized response generation.

    Intended for create, update, or custom workflow actions not directly tied to a model.
    """

    def get_process_body_data(self, request: Request, *args, **kwargs) -> Dict:
        """
        Consolidates input data from multiple request sources.

        Priority: Multipart form data > Request body > Query params > URL kwargs.

        Args:
            request (Request): The incoming DRF request object.
            *args: Positional arguments (not used directly).
            **kwargs: Additional route parameters.

        Returns:
            Dict: Merged and flattened data for serializer consumption.
        """
        content_type = request.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            # Form uploads (files or form fields) are handled directly
            return request.data

        # Merge JSON body, query parameters, and any route kwargs
        return {**request.data, **request.GET.dict(), **kwargs}

    def process_serializer(self) -> Serializer:
        """
        Prepares and returns a serializer instance populated with request data and context.

        Returns:
            Serializer: Initialized serializer instance ready for validation and processing.
        """
        context: Dict = self.set_context_data()
        serializer_class: Serializer = self.get_serializer(
            data=self.get_process_body_data(request=self.request), context=context
        )
        return serializer_class

    def handle_process_request(self) -> Response:
        """
        Validates serializer input and executes serializer's `create()` method.

        Returns:
            Response: A success response with serialized output or a validation error response.
        """
        serializer_class: Serializer = self.process_serializer()
        # ? this is drf validation by serializer
        serializer_errors: bool = serializer_class.is_valid()
        is_serializer_validated: bool

        if serializer_errors:
            is_serializer_validated: bool = True
            # if serializer is valid then validation data is Object data serialized by serializer
            validated_data: Dict = serializer_class.api_data
        else:
            is_serializer_validated: bool = False
            # if serializer is not valid then validation data is raw data
            validated_data: Dict = self.request.data
        # ? this is to validated_data from handler validation
        if not is_serializer_validated:
            validated_data: Dict = serializer_class.validate(validated_data)
        validated_data: Dict = serializer_class.api_data
        if validated_data.get("error_message", {}):
            # API-level errors passed through validated_data
            return self.validation_response(validated_data=validated_data)
        if not validated_data and self.request.data and self.request.data.dict():
            # api_data missing or None
            error_message: Dict = {
                "error_message": "api_data is None",
            }
            return self.validation_response(validated_data=error_message)

        # if not serializer_errors:
        #     # Return validation error if input data is invalid
        #     error_message: Dict = {
        #         "error_message": {
        #             "message": CORE_UTILS_DEV_ERROR_MESSAGE,
        #             "description": "Serializer validation failed",
        #             "error": serializer_class.errors,
        #         }
        #     }
        #     return self.validation_response(validated_data=error_message)
        # Remove error_message if it's clean
        validated_data.pop("error_message", None)

        # Delegate logic to serializer's create method
        response_data: Dict = serializer_class.create(validated_data)
        if validated_data.get("toast_message_value"):
            self.set_toast_message_value(value=validated_data["toast_message_value"])

        if validated_data.get("activity_log_instance"):
            self.set_activity_log_instance(
                instance=validated_data["activity_log_instance"]
            )
        return self.success_response(validated_data=response_data)

    def handle_request(self) -> Response:
        """
        Safely wraps the main data processing logic with exception handling.

        Returns:
            Response: DRF response object with success or error information.
        """
        try:
            return self.handle_process_request()
        except Exception as e:
            return self.custom_handle_exception(e=e)

    def get_data_from_serializer(self) -> Dict:
        """
        Validates and processes serializer logic to return raw or paginated response data.

        Returns:
            Dict: Either a paginated dictionary or validation error structure.
        """
        serializer_class: Serializer = self.process_serializer()
        serializer_errors: bool = serializer_class.is_valid()

        if not serializer_errors:
            error_message: Dict = {
                "error_message": {
                    "title": CORE_UTILS_DEV_ERROR_MESSAGE,
                    "description": "Serializer validation failed",
                    "error": serializer_class.errors,
                }
            }
            return self.validation_response(validated_data=error_message)

        validated_data: Dict = serializer_class.api_data

        if not validated_data:
            error_message: Dict = {
                "error_message": {
                    "title": CORE_UTILS_DEV_ERROR_MESSAGE,
                    "description": "api_data is None",
                }
            }
            return self.validation_response(validated_data=error_message)

        if validated_data.get("error_message", {}):
            return self.validation_response(validated_data=validated_data)

        # Remove unused error_message
        validated_data.pop("error_message", None)

        # Return paginated data using serializer logic
        response_data: Dict = serializer_class.create(validated_data)
        return self.get_paginated_response(response_data)

    def get_custom_response(self) -> Response:
        """
        Validates serializer input and executes serializer's `create()` method.

        Returns:
            Response: A success response with serialized output or a validation error response.
        """
        serializer_class: Serializer = self.process_serializer()
        # ? this is drf validation by serializer
        serializer_errors: bool = serializer_class.is_valid()
        is_serializer_validated: bool

        if serializer_errors:
            is_serializer_validated: bool = True
            # if serializer is valid then validation data is Object data serialized by serializer
            validated_data: Dict = serializer_class.api_data
        else:
            is_serializer_validated: bool = False
            # if serializer is not valid then validation data is raw data
            validated_data: Dict = self.request.data
        # ? this is to validated_data from handler validation
        if not is_serializer_validated:
            validated_data: Dict = serializer_class.validate(validated_data)
        validated_data: Dict = serializer_class.api_data
        if validated_data.get("error_message", {}):
            # API-level errors passed through validated_data
            return self.validation_response(validated_data=validated_data)
        if not validated_data and self.request.data and self.request.data.dict():
            # api_data missing or None
            error_message: Dict = {
                "error_message": "api_data is None",
            }
            return self.validation_response(validated_data=error_message)
        if not serializer_errors:
            # Return validation error if input data is invalid
            error_message: Dict = {
                "error_message": {
                    "message": CORE_UTILS_DEV_ERROR_MESSAGE,
                    "description": "Serializer validation failed",
                    "error": serializer_class.errors,
                }
            }
            return self.validation_response(validated_data=error_message)
        # Remove error_message if it's clean
        validated_data.pop("error_message", None)

        # Delegate logic to serializer's create method
        response_data: Dict = serializer_class.create(validated_data)
        if validated_data.get("toast_message_value"):
            self.set_toast_message_value(value=validated_data["toast_message_value"])
        return self.success_response(validated_data=response_data["results"])


class CoreGenericProcessDataModelSerializerAPIView(CoreGenericQuerysetInstance):
    """
    A specialized base view for updating model instances using model-bound serializers.

    Retrieves the target model instance, applies request data to it, and invokes serializer logic.
    Suitable for PUT/PATCH operations that involve modifying a single object.
    """

    def process_serializer(self) -> Serializer:
        """
        Prepares a model-bound serializer with the instance to update and incoming request data.

        Returns:
            Serializer: DRF serializer preloaded with an instance and new data.
        """
        context: Dict = self.set_context_data()

        serializer_class: Serializer = self.get_serializer(
            instance=self.get_object(),  # Load object to update
            data=self.get_process_body_data(request=self.request),
            many=False,
            context=context,
        )
        return serializer_class
