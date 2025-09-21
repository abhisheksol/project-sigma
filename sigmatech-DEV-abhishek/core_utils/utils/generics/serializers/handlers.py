from django.db.models.query import QuerySet
from django.db.models import Model
from rest_framework.request import Request
from typing import Dict


class CoreGenericMultiDeleteHandler:
    """
    Handles custom multi-delete validation and execution logic for queryset objects.
    """

    request: Request
    data: Dict
    queryset: QuerySet[Model] = None

    def __init__(self, request: Request, queryset: QuerySet):
        """
        Initializes the delete handler with request and queryset context.

        Args:
            request (Request): DRF request instance.
            queryset (QuerySet): Model queryset to perform deletion on.
        """
        self.request = request
        self.queryset = queryset

    def set_data(self, data: Dict):
        """
        Stores incoming data for processing.

        Args:
            data (Dict): Payload containing IDs for deletion.
        """
        self.data = data

    def validate(self):
        """
        Validates whether provided delete IDs exist in the queryset.
        Adds error message to data if validation fails.
        """
        if not self.queryset.filter(pk__in=self.data["delete_id"]).exists():
            self.data["error_message"] = {
                "title": "Delete ID",
                "description": "One or more provided delete IDs are invalid.",
            }

    def create(self):
        """
        Executes deletion of objects with provided primary keys.
        """
        self.queryset.filter(pk__in=self.data["delete_id"]).delete()
