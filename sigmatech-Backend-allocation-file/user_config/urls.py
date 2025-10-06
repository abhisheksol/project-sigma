from typing import List

from django.urls import include, path

urlpatterns: List = [
    path("user-auth/", include("user_config.user_auth.urls")),
    path("accounts/", include("user_config.accounts.urls")),
    path("permissions/", include("user_config.permissions.urls")),
]
