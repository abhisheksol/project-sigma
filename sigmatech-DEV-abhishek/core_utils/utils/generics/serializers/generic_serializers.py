from rest_framework import serializers
from django.db.models import QuerySet, Model


class CoreGenericGetQuerysetSerializer:
    """
    Provides a base method to retrieve the queryset for serializers.
    """

    def get_queryset(self) -> QuerySet[Model]:
        """
        Retrieves the queryset from the class attribute or model.

        Returns:
            QuerySet[Model]: The queryset for the serializer.

        Raises:
            Exception: If neither queryset nor Meta.model is defined.
        """
        try:
            if hasattr(self, "queryset") and self.queryset is not None:
                return self.queryset.all()
            return self.Meta.model.objects.all()
        except:
            print("Queryset is not defined for the serializer.")


class CoreGenericMultipleObjectDeleteSerializer(CoreGenericGetQuerysetSerializer):
    """
    Serializer to validate and delete multiple model instances by primary key.
    """

    INCORRECT_DELETE_ID_ERROR_MESSAGE = "Incorrect Delete ID(s) provided."

    def validate(self, data: dict):
        """
        Validates that all provided delete IDs exist in the queryset.

        Args:
            data (dict): Data containing delete_id list.

        Returns:
            dict: Validated data.

        Raises:
            ValidationError: If any delete ID does not exist.
        """
        if self.get_queryset().filter(pk__in=data["delete_id"]).count() != len(
            data["delete_id"]
        ):
            raise serializers.ValidationError(self.INCORRECT_DELETE_ID_ERROR_MESSAGE)
        return data

    def create(self, validated_data: dict):
        """
        Deletes objects matching the validated delete IDs.

        Args:
            validated_data (dict): Validated data with delete_id list.

        Returns:
            dict: Same validated data after deletion.
        """
        self.get_queryset().filter(pk__in=validated_data["delete_id"]).delete()
        return validated_data


class CoreGenericHelperAPISerializerMethodField:
    def get_disabled(self, obj: Model):
        return obj.status and obj.status == "DEACTIVATED"
