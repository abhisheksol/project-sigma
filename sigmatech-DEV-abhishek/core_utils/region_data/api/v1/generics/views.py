from rest_framework import generics, filters, permissions
from core_utils.utils.generics.views.generic_views import CoreGenericListAPIView
from core_utils.region_data.api.v1.utils.filterset import CityFilterSet, StateFilterSet

from core_utils.region_data.models import (
    CityModel,
    CountryModel,
    StateModel,
    CountryMobileCodesModel,
)
from .serializers import (
    CityModelSerializer,
    CountryMobileCodesModelSerializer,
    CountryModelSerializer,
    StateModelSerializer,
)

import django_filters.rest_framework
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class CountryListAPIView(CoreGenericListAPIView, generics.ListAPIView):
    """
    API view to retrieve a list of countries.

    - Supports search filtering on `name`.
    - Requires authenticated access using `CustomAuthentication`.
    - Inherits from `CoreGenericGetAPIView` for common GET handling.
    """

    queryset = CountryModel.objects.all().order_by("name")
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class used for GET requests.
        """
        serializer_class = {
            "GET": CountryModelSerializer,
        }

        return serializer_class.get(self.request.method)


class StateListAPIView(CoreGenericListAPIView, generics.ListAPIView):
    """
    API view to retrieve a list of states.

    - Supports search and filtering via `StateFilterSet`.
    - Requires authentication via `CustomAuthentication`.
    """

    queryset = StateModel.objects.all().order_by("name")
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = StateFilterSet
    search_fields = ["name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class used for GET requests.
        """
        serializer_class = {
            "GET": StateModelSerializer,
        }

        return serializer_class.get(self.request.method)


class CityListViewAPIView(CoreGenericListAPIView, generics.ListAPIView):
    """
    API view to retrieve a list of cities.

    - Allows filtering by `CityFilterSet` and search by `name`.
    - Requires authenticated access.
    """

    queryset = CityModel.objects.all().order_by("name")
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = CityFilterSet
    search_fields = ["name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class used for GET requests.
        """
        serializer_class = {
            "GET": CityModelSerializer,
        }

        return serializer_class.get(self.request.method)


class CountryMobileCodesModelAPIView(CoreGenericListAPIView, generics.ListAPIView):
    """
    API view to retrieve a list of country mobile codes.

    - Searchable by `title` field.
    - Requires user authentication.
    """

    queryset = CountryMobileCodesModel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class used for GET requests.
        """
        serializer_class = {
            "GET": CountryMobileCodesModelSerializer,
        }

        return serializer_class.get(self.request.method)
