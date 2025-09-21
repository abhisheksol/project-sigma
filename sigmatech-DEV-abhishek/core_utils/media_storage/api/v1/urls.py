from django.urls import path
from core_utils.media_storage.api.v1.file_convertion import (
    views as file_convertion_views,
)
from typing import List

file_convertion_urlpatterns: List = [
    path(
        "live-kit-file-to-url/",
        file_convertion_views.LiveKitFileToUrlConversionAPIView.as_view(),
        name="FileToUrlConversionAPIView",
    ),
    path(
        "file-to-url/",
        file_convertion_views.FileToUrlConversionAPIView.as_view(),
        name="FileToUrlConversionAPIView",
    ),
]

urlpatterns: List = [*file_convertion_urlpatterns]
