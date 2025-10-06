from django.urls import path, include
from typing import List


urlpatterns: List = [
    path("case-management/", include("store.operations.case_management.urls")),
    path("api/v1/", include("store.operations.allocation_files.v1.urls")),
    path("api/v1/", include("store.operations.referal_files.urls")),
]
