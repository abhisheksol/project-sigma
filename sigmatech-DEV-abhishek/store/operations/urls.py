from django.urls import path, include
from typing import List


urlpatterns: List = [
    path("case-management/", include("store.operations.case_management.urls")),
    path("allocation-files/", include("store.operations.allocation_files.urls")),
    # path("referal-files/", include("store.operations.referal_files.urls")),
]
