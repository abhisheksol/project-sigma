from core_utils.activity_monitoring.api.v1.generics.serializers import (
    ActivityMethodEnumHelperListEnumSerializer,
    ActivityMonitoringLinkedEntityModelSerializer,
    ActivityMonitoringLogListModelSerializer,
    ActivityTypeHelperListModelSerializer,
)
from core_utils.activity_monitoring.api.v1.generics.utils.filters import (
    ActivityMonitoringLogFilterSet,
)
from core_utils.activity_monitoring.models import (
    ActivityMonitoringLinkedEntityModel,
    ActivityMonitoringLogModel,
    ActivityTypeModel,
)
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericGetDataFromSerializerAPIView,
    CoreGenericListCreateAPIView,
)
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class ActivityMonitoringLogListModelGenericAPIView(
    CoreGenericListCreateAPIView, generics.ListAPIView
):
    queryset = ActivityMonitoringLogModel.objects.all()
    authentication_classes = [CustomAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["activity_type__lable", "description"]
    filterset_class = ActivityMonitoringLogFilterSet

    def get_queryset(self):
        return self.queryset.all()

    def get_serializer_class(self):

        return {
            "GET": ActivityMonitoringLogListModelSerializer,
        }.get(self.request.method)


class ActivityMonitoringLinkedEntityHelperGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = ActivityMonitoringLinkedEntityModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by("title")

    def get_serializer_class(self):

        return {
            "GET": ActivityMonitoringLinkedEntityModelSerializer,
        }.get(self.request.method)


class ActivityTypeHelperListGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView,
):
    queryset = ActivityTypeModel.objects.all().order_by("title")
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        params: dict = self.request.GET.dict()
        if params.get("linked_entity"):
            return self.queryset.filter(linked_entity__pk=params["linked_entity"])
        return self.queryset.all()

    def get_serializer_class(self):
        return {
            "GET": ActivityTypeHelperListModelSerializer,
        }.get(self.request.method)


class ActivityMethodEnumHelperListEnumAPIView(
    CoreGenericGetDataFromSerializerAPIView,
    generics.GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": ActivityMethodEnumHelperListEnumSerializer,
        }.get(self.request.method)
