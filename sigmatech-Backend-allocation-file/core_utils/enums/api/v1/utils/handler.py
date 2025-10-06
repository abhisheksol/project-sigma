from core_utils.enums.api.v1.utils.enum_list import PROJECT_CONFIG_ENUM_CLASSES
from core_utils.utils.enums import list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from typing import List, Optional


class EnumHelperListHandler(CoreGenericBaseHandler):
    """
    Handler to retrieve a list of enum values for a given enum class.

    This handler validates the input `enum_class`, ensures it exists in the
    project configuration enums, and prepares a list of dictionaries containing
    `value` and `label` keys for each enum item.
    """

    def validate(self):
        """
        Validates the input data for the handler.

        Checks:
        1. 'enum_class' is provided in self.data.
        2. 'enum_class' is valid and exists in PROJECT_CONFIG_ENUM_CLASSES.

        Sets an error message using `self.set_error_message` if validation fails.
        """
        # Get the enum class from input data
        enum_class: Optional[str] = self.data.get("enum_class")

        # Ensure enum_class is provided
        if not enum_class:
            return self.set_error_message(
                key="enum_class",
                error_message="enum_class is required",
            )

        # Ensure enum_class is valid
        if not PROJECT_CONFIG_ENUM_CLASSES.get(enum_class):
            return self.set_error_message(
                key="enum_class",
                error_message="enum_class is invalid",
            )

    def create(self):
        """
        Prepares the list of enum values for the given enum_class.

        The result is stored in self.data['results'] as a list of dictionaries:
        [
            {"value": enum, "label": enum},
            ...
        ]
        where both 'value' and 'label' are the enum values returned by `list_enum_values`.
        """
        # Get the enum values for the given enum_class
        enum_class_values: List[str] = PROJECT_CONFIG_ENUM_CLASSES[
            self.data["enum_class"]
        ]

        # Prepare results in the expected format
        self.data["results"] = [
            {"value": enum, "label": enum}
            for enum in list_enum_values(enum_cls=enum_class_values)
        ]
