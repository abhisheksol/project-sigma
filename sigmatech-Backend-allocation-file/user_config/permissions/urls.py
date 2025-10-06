from django.urls import path, include

urlpatterns: list = [path("api/v1/", include("user_config.permissions.api.v1.urls"))]
