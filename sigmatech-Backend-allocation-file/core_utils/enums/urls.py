from django.urls import path, include

urlpatterns = [path("api/v1/", include("core_utils.enums.api.v1.urls"))]
