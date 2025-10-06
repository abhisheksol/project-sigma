from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from core_utils.utils.generics.views.generic_views import (
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
)
from core_utils.notifications.models import NotificationModel
from core_utils.notifications.api.v1.utils.constants import (
    NOTIFICATIONS_SUCCESS_MESSAGE,
)
from core_utils.notifications.api.v1.utils.filters import NotificationModelFilterSet
from core_utils.notifications.api.v1.serializers import (
    CoreUtilsNotificationModelListSerializer,
    CoreUtilsNotificationModelUpdateSerializer,
)


class CoreUtilsNotificationModelGenericAPIView(
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset = NotificationModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    success_message = NOTIFICATIONS_SUCCESS_MESSAGE

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = NotificationModelFilterSet

    def get_queryset(self):
        return self.queryset.filter(
            is_deleted=False,
            user=self.request.user,
            company=self.get_company_instance(),
        )

    def get_serializer_class(self):
        serializer_class = {
            "GET": CoreUtilsNotificationModelListSerializer,
            "PUT": CoreUtilsNotificationModelUpdateSerializer,
        }

        return serializer_class.get(self.request.method)
