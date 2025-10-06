from rest_framework import permissions
from rest_framework.views import APIView
from typing import List

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path, path

from decouple import config

"""
    Swagger/OpenAPI schema view configuration using drf-yasg
"""

schema_view: APIView = get_schema_view(
    openapi.Info(
        title=config("SWAGGER_TITLE"),  # * e.g., "My API"
        default_version=config("SWAGGER_API_VERSION"),  # * e.g., "v1"
        description=config("SWAGGER_DESCRIPTION"),  # * API description
        terms_of_service=config("SWAGGER_TERMS_OF_SERVICE"),  # * Link to ToS
        contact=openapi.Contact(
            email=config("SWAGGER_CONTACT_EMAIL")
        ),  # * Support contact
        license=openapi.License(name=config("SWAGGER_LICENSE")),  # * e.g., "MIT"
    ),
    public=True,
    # ? Allow all users to access docs
    permission_classes=[permissions.AllowAny],
)

"""
    Swagger and ReDoc URL patterns for API documentation
    These routes will only be enabled in development environment
"""

# ? Default Swagger URL patterns
urlpattern: List = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "swagger/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

# ? Empty by default; conditionally set if environment is development
swagger_urlpatter: List = []

# ? Enable Swagger routes only if SERVER_TYPE is set to "DEV"
if config("SERVER_TYPE") == "DEV":
    swagger_urlpatter: List = urlpattern
