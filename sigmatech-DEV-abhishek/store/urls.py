from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("configurations/", include("store.configurations.urls")),
    path("operations/", include("store.operations.urls")),
    path("paidfile/", include("store.paidfile.v1.generic.urls")),
]
