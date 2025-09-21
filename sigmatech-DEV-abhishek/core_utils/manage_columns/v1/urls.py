from django.urls import path

from core_utils.manage_columns.v1.generics import views

from typing import List

urlpatterns: List = [
    path(
        "manage-column-api/",
        views.GenericUserConfigManageColumnAPIView.as_view(),
        name="GenericUserConfigManageColumnAPIView",
    )
]
