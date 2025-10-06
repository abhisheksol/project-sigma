from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("api/v1/", include("core_utils.notifications.api.v1.urls")),
]
