from django.urls import path
from typing import List
from core_utils.enums.api.v1.helper_api.views import EnumsHelperListAPIView

urlpatterns: List[path] = [
    path(
        "enums-helper-list-api/",
        EnumsHelperListAPIView.as_view(),
        name="EnumsHelperGenericAPIView",
    )
]
