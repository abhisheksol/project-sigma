from django.db.models.query import QuerySet
from django.db.models import Model
from typing import Dict, Type, Callable, Optional
from rest_framework.request import Request
from core_utils.utils.db_utils.update_instance import CoreGenericCrudHandlerUtils
from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericGetQuerysetSerializer,
)


class CoreGenericSerializerMixin(CoreGenericGetQuerysetSerializer):
    """
    A reusable mixin to integrate custom validator and creation logic
    for Django REST Framework (DRF) serializers.

    This mixin leverages an external handler class (provided by `handler_class`)
    to handle validation and object creation, enabling separation of logic from the serializer.

    Attributes:
        custom_validator (Type): The instantiated handler class.
        queryset (QuerySet[Model]): Queryset used for validations.
        api_data (dict): Validated data shared between serializer and handler.
        handler_class (Type): Class that contains validation and creation logic.
    """

    custom_validator: Type
    queryset: QuerySet[Model]
    api_data: Dict = {}
    handler_class: Type  # Must be set in subclass

    def set_validator(self):
        """
        Instantiates the handler class using request and queryset.

        Returns:
            Type: Initialized handler instance with context.
        """
        self.custom_validator = self.handler_class(
            request=self.context["request"],
            queryset=self.get_queryset(),
            context=self.context,
        )
        return self.custom_validator

    def custom_validate(self, data: Dict):
        """
        Invokes custom validation logic defined in the handler.

        Args:
            data (Dict): Input data from the serializer.
        """
        self.set_validator()
        self.custom_validator.set_data(data=data)
        self.custom_validator.validate()
        self.api_data = data  # Optionally retained for further use

    def validate(self, data: Dict):
        """
        Overrides DRF’s `validate()` method to use custom validator logic.

        Args:
            data (Dict): Input serializer data.

        Returns:
            Dict: Validated data.
        """
        self.custom_validate(data)
        return data

    def create(self, validated_data: Dict):
        """
        Triggers the handler's `create()` method to execute creation logic.

        Args:
            validated_data (Dict): Data that passed validation.

        Returns:
            Dict: The same validated data (after creation logic).
        """
        self.custom_validator.create()
        return validated_data


class CoreGenericBaseHandler(CoreGenericCrudHandlerUtils):
    """
    Base handler class for encapsulating custom validation and business logic.

    This class is used in conjunction with serializers to offload
    validation, error handling, and processing logic from the serializer.

    Note:
        - Designed to be subclassed by handler classes.
        - Should be inherited first if multiple inheritance is used.

    Attributes:
        request (Request): DRF request instance.
        data (Dict): Validated data passed from the serializer.
        queryset (QuerySet[Model]): Optional queryset context.
    """

    request: Request
    data: Dict
    queryset: QuerySet[Model]
    context: Dict

    def __init__(self, request: Request, queryset: QuerySet, context: Dict):
        """
        Initializes the handler with the request and queryset context.

        Args:
            request (Request): DRF request object.
            queryset (QuerySet): Queryset relevant to the current context.
        """
        self.request: Request = request
        self.queryset: QuerySet = queryset
        self.context: Dict = context

    def set_data(self, data: Dict):
        """
        Sets the validated data from the serializer into the handler.

        Args:
            data (Dict): Data passed from serializer post-validation.
        """

        self.data = data

    def set_error_message(
        self, error_message: Dict, key: str = "", is_field_errors: bool = False
    ):
        """
        Sets an error message to the handler's data object.

        Args:
            error_message (Dict): Dict with 'title' and 'description'.
            key (str): Optional field key if it's a field-level error.
            is_field_errors (bool): Flag to specify field-level or global error.
        """
        if key:
            if is_field_errors:
                error_message: Dict = key + " " + error_message["description"]
            # Initialize field_errors dict if not present
            if not self.data.get("field_errors"):
                self.data["field_errors"] = {}
            # Assign error to specific field
            self.data["field_errors"][key] = error_message
        # Set global error message
        self.data["error_message"] = error_message

    def get_request_kwargs(self) -> Dict:
        """
        Extracts the keyword arguments from the DRF request's parser context.

        Returns:
            Dict: The `kwargs` dictionary from the current request context.
        """
        return self.request.parser_context["kwargs"]

    def required_field_validation(self) -> Optional[Dict[str, str]]:
        """
        Validate that all required fields are provided.

        Returns:
            Optional[Dict[str, str]]: Error message with the missing key if validation fails,
                                      None otherwise.
        """
        for key in self.required_fields.keys():
            if not self.data.get(key):
                return {
                    "error_message": self.required_fields[key],
                    "key": key,
                }

    def is_valid(
        self, validation_methods: Optional[Dict[Callable, Dict]]
    ) -> Optional[Dict[str, str]]:
        """
        Run all validation methods in sequence until one fails.

        Returns:
             -> Optional[Dict[str, str]]: Dict if error exists
        """
        for method, args in enumerate(validation_methods()):
            result: Optional[Dict[str, str]] = method(**args)
            if result:
                return result
