from django.urls import path, include
from typing import List

urlpatterns: List = [
    path("configurations/", include("store.configurations.urls")),
    path("operations/", include("store.operations.urls")),
    # path("timepass/", include("store.timepass.api.v1.generic.urls")),
    path("CaseManagement/", include("store.operations.case_management.v1.generic.urls"))
]
