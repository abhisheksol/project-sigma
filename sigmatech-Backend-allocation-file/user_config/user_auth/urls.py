from typing import List

from django.urls import include, path

urlpatterns: List = [path("api/v1/", include("user_config.user_auth.api.v1.urls"))]
