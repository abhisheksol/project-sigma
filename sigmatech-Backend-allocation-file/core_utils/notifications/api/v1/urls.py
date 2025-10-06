from django.urls import path
from typing import List
from . import views as notification_views

urlpatterns: List = [
    path(
        "notifications-generic-api/",
        notification_views.CoreUtilsNotificationModelGenericAPIView.as_view(),
        name="CoreUtilsNotificationModelGenericAPIView",
    ),
]
