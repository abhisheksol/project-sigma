from django.urls import path
from typing import List
from store.operations.allocation_files.v1.generics import views as generic_views
from store.operations.allocation_files.v1.helper_apis import views as helper_views


generic_urlpatterns: List = [
    path(
        "allocation-file-api/",
        generic_views.AllocationFileGenericAPIView.as_view(),
        name="AllocatinFileGenericAPIView",
    ),
    path(
        "allocation-file-api/<str:id>/",
        generic_views.AllocationFileDetailAPIView.as_view(),
        name="AllocationFileDetailModelSerializer",
    ),
]

helper_list_urlpatterns: List = [
    path(
        "allocation-file-status-helper/",
        helper_views.AllocationFileStatusHelperGenericAPIView.as_view(),
        name="AllocationFileStatusHelperAPIView",
    ),
    path(
        "allocation-file-helper/",
        helper_views.AllocationFileHelperGenericAPIView.as_view(),
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
