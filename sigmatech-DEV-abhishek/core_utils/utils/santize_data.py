from django.db import models
from typing import Dict
from django.core.serializers import serialize
import json


def object_to_json(instance: models.Model) -> Dict:
    if not instance:
        return {}

    # Serialize the instance to JSON string in dumpdata format
    serialized_str = serialize("json", [instance])

    # Load the string back to Python data structure
    data = json.loads(serialized_str)

    # Return the first (and only) item in the list as Dict
    return data[0]
