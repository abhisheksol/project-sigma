from django.urls import path
from typing import List
from store.operations.allocation_files.v1.generics import views as generic_views
from store.operations.allocation_files.v1.helper_apis import views as helper_views


# ! make it generic_utrl pattern
generic_urlpatterns: List = [
    path(
        "allocation-file-api/",
        generic_views.AllocationFileGenericAPIView.as_view(),
        name="AllocatinFileGenericAPIView",
    )
]

helper_list_urlpatterns: List = [
    path(
        "allocation-file-status-helper/",
        helper_views.AllocationFileStatusHelperGenericAPIView.as_view(),
        name="AllocationFileStatusHelperAPIView",
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
