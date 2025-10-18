from django.urls import path
from typing import List
from store.operations.case_management.v1.generics import views as generic_views
from store.operations.case_management.v1.helper_apis import views as helper_views


generic_urlpatterns: List = [
    path(
        "case-allocation-file-api/",
        generic_views.CaseallocationGenericAPIView.as_view(),
        name="AllocatinFileGenericAPIView",
    )
]

helper_list_urlpatterns: List = [
    path(
        "case-allocation-risk-file-status-helper/",
        helper_views.CaseALLocationRiskHelperGenericAPIView.as_view(),
        name="AllocationFileStatusHelperAPIView",
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
