from django.urls import path, include
from typing import List


urlpatterns: List = [
    path("api/v1/", include("store.operations.allocation_files.v1.urls")),
]
