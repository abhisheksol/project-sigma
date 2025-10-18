from django.urls import path, include
from typing import List


urlpatterns: List = [
    path("api/v1/", include("store.operations.case_management.v1.urls")),
    # path("referal-files/", include("store.operations.referal_files.urls")),
]
