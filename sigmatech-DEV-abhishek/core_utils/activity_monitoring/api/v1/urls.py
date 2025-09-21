from django.urls import path

from core_utils.activity_monitoring.api.v1.generics import views


urlpatterns: list = [
    path(
        "activity-monitoring-list-api/",
        views.ActivityMonitoringLogListModelGenericAPIView.as_view(),
        name="ActivityMonitoringLogListModelGenericAPIView",
    ),
    path(
        "activity-monitoring-linked-entity-helper-list-api/",
        views.ActivityMonitoringLinkedEntityHelperGenericAPIView.as_view(),
        name="ActivityMonitoringLinkedEntityHelperGenericAPIView",
    ),
    path(
        "activity-monitoring-activity-type-helper-list-api/",
        views.ActivityTypeHelperListGenericAPIView.as_view(),
        name="ActivityTypeHelperListGenericAPIView",
    ),
    path(
        "activity-monitoring-activity-method-helper-list-api/",
        views.ActivityMethodEnumHelperListEnumAPIView.as_view(),
        name="ActivityMethodEnumHelperListEnumAPIView",
    ),
]
