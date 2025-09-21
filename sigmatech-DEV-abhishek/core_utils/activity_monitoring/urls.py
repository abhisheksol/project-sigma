from django.urls import path, include


urlpatterns: list = [
    path("api/v1/", include("core_utils.activity_monitoring.api.v1.urls"))
]
