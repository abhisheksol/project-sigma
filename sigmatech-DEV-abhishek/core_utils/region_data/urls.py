from django.urls import path, include
from typing import List

urlpatterns: List = [path("api/v1/", include("core_utils.region_data.api.v1.urls"))]
