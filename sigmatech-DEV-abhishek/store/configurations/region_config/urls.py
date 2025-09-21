#  path("region-config/", include("store.configurations.region_config.urls")),

from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("api/v1/", include("store.configurations.region_config.api.v1.urls"))
]
