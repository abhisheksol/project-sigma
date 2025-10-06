from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("region-data/", include("core_utils.region_data.api.v1.urls")),
    path("activity-monitoring/", include("core_utils.activity_monitoring.urls")),
    path("manage-columns/", include("core_utils.manage_columns.v1.urls")),
    path("enums/", include("core_utils.enums.urls")),
]
