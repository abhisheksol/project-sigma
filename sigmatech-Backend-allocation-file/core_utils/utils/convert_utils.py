from django.db.models import Model
from typing import List, Dict, Any


def get_values_from_list_of_queryset(
    queryset: List[Model], values_list: List[str]
) -> List[Dict[str, Any]]:
    """
    Extracts specific field values from a list of Django model instances.

    Args:
        queryset (List[Model]):
            A list of Django model instances (e.g., queryset results).
        values_list (List[str]):
            A list of field names (as strings) whose values should be extracted
            from each model instance.

    Returns:
        List[Dict[str, Any]]:
            A list of dictionaries where each dictionary represents one model
            instance, containing key-value pairs of the requested fields.

    Example:
        Suppose you have a queryset of `User` model instances and you want only
        the `id` and `email` fields:

        >>> get_values_from_list_of_queryset(users, ["id", "email"])
        [
            {"id": 1, "email": "test1@example.com"},
            {"id": 2, "email": "test2@example.com"},
            ...
        ]
    """
    result: List[Dict[str, Any]] = []

    # Loop through each model instance in the queryset
    for query in queryset:
        instance: Dict[str, Any] = {}

        # Extract each requested field from the model instance
        for value in values_list:
            # getattr is used to safely get the attribute (returns None if missing)
            instance_value: Any = getattr(query, value, None)
            if instance_value:
                instance[value] = str(instance_value)
            else:
                instance[value] = instance_value

        # Append the dictionary for this instance to the result list
        result.append(instance)

    return result
