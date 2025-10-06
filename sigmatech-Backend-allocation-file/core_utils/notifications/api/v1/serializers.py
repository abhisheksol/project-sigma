from rest_framework import serializers
from core_utils.notifications.models import NotificationModel
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from core_utils.notifications.api.v1.utils.handlers.notification_update_handler import (
    CoreUtilsNotificationModelUpdateHandler,
)


class CoreUtilsNotificationModelListSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing Notifications
    """

    notification_type__id = serializers.IntegerField(
        source="notification_type.pk", default=None
    )
    notification_type__title = serializers.CharField(
        source="notification_type.title", default=None
    )
    mentioned_by__username = serializers.CharField(
        source="mentioned_by.username", default=None
    )
    mentioned_by__profile_pic = serializers.URLField(
        source="mentioned_by.UserDetailModel_user.profile_pic", default=None
    )

    class Meta:
        model = NotificationModel
        fields = (
            "id",
            "notification_type__id",
            "notification_type__title",
            "title",
            "message",
            "is_read",
            "read_at",
            "is_cleared",
            "cleared_at",
            "mentioned_by__username",
            "mentioned_by__profile_pic",
            "core_generic_created_at",
            "notification_icon",
            "is_routing",
            "route_data",
        )


class CoreUtilsNotificationModelUpdateSerializer(
    CoreGenericSerializerMixin,
    serializers.ModelSerializer,
):
    """
    Serializer for Updating Notifications
    """

    handler_class = CoreUtilsNotificationModelUpdateHandler
    mark_as_read = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, required=False
    )
    mark_as_cleared = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, required=False
    )
    mark_all_as_read = serializers.BooleanField(default=False)
    mark_all_as_cleared = serializers.BooleanField(default=False)
    tab = serializers.IntegerField()

    class Meta:
        model = NotificationModel
        fields = (
            "mark_as_read",
            "mark_as_cleared",
            "mark_all_as_read",
            "mark_all_as_cleared",
            "tab",
        )
