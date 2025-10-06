from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("api/v1/", include("store.configurations.loan_config.api.v1.urls"))
]
