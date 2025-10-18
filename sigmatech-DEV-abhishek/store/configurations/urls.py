from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("loan-config/", include("store.configurations.loan_config.urls")),
    path("region-config/", include("store.configurations.region_config.urls")),
    path(
        "fo-assignment-rules/", include("store.configurations.fo_assignment_rules.urls")
    ),
]
