from typing import Type, List
import importlib
from types import ModuleType
from rest_framework import serializers, generics


def string_to_serializer(serializer_string: str) -> Type[serializers.Serializer]:
    """
    Convert a string path to a Django REST Framework serializer class.

    Args:
        serializer_string (str): The full path to the serializer class (e.g., 'path.to.module.SerializerClass').

    Returns:
        Type[serializers.Serializer]: The serializer class.

    Raises:
        ValueError: If the serializer string is invalid or the class is not a serializer.
        TypeError: If the resolved class is not a valid serializer subclass.
    """
    try:
        module_name: str
        serializer_name: str
        module_name, serializer_name = serializer_string.rsplit(".", 1)

        # Import the module
        module_obj: ModuleType = importlib.import_module(module_name)

        # Get the serializer class
        serializer_class: Type = getattr(module_obj, serializer_name)

        # Validate that it's a serializer class
        if not (
            isinstance(serializer_class, type)
            and (
                issubclass(serializer_class, serializers.Serializer)
                or issubclass(serializer_class, serializers.ModelSerializer)
            )
        ):
            raise TypeError(f"Class '{serializer_name}' is not a valid serializer.")

        return serializer_class

    except (ValueError, AttributeError, ImportError) as e:
        raise ValueError(
            f"Unable to load serializer from string '{serializer_string}': {str(e)}"
        )


def string_to_view(view_name_string: str) -> Type[generics.GenericAPIView]:
    """
    Convert a string path to a Django REST Framework view class.

    Args:
        view_name_string (str): The full path to the view class (e.g., 'path.to.module.ViewClass').

    Returns:
        Type[generics.GenericAPIView]: The view class.

    Raises:
        ValueError: If the view string is invalid or the class is not a view.
        TypeError: If the resolved class is not a valid view subclass.
    """
    try:
        module_name: str
        view_name: str
        module_name, view_name = view_name_string.rsplit(".", 1)

        # Import the module
        module_obj: ModuleType = importlib.import_module(module_name)

        # Get the view class
        view_class: Type = getattr(module_obj, view_name)

        # Validate that it's a view class
        if not (
            isinstance(view_class, type)
            and (
                issubclass(view_class, generics.ListCreateAPIView)
                or issubclass(view_class, generics.GenericAPIView)
            )
        ):
            raise TypeError(f"Class '{view_name}' is not a valid view class.")

        return view_class

    except (ValueError, AttributeError, ImportError) as e:
        raise ValueError(
            f"Unable to load view from string '{view_name_string}': {str(e)}"
        )


def get_keys_of_serializer(serializer_string: str) -> List[str]:
    """
    Extract the field names from a serializer class specified by its string path.

    Args:
        serializer_string (str): The full path to the serializer class (e.g., 'path.to.module.SerializerClass').

    Returns:
        List[str]: A list of field names defined in the serializer.

    Raises:
        ValueError: If the serializer string is invalid or cannot be loaded.
    """
    # Get the serializer class
    serializer_class: Type[serializers.Serializer] = string_to_serializer(
        serializer_string
    )

    # Instantiate the serializer
    serializer_instance: serializers.Serializer = serializer_class()

    # Get the field names
    fields: List[str] = list(serializer_instance.get_fields().keys())

    return fields
