from django.urls import path
from core_utils.region_data.api.v1.generics import views as generic_list_api_views
from typing import List

urlpatterns: List = [
    path(
        "countries-api/",
        generic_list_api_views.CountryListAPIView.as_view(),
        name="CountryListAPIView",
    ),
    path(
        "states-api/",
        generic_list_api_views.StateListAPIView.as_view(),
        name="StateListAPIView",
    ),
    path(
        "cities-api/",
        generic_list_api_views.CityListViewAPIView.as_view(),
        name="CityListViewAPIView",
    ),
    path(
        "country-codes-api/",
        generic_list_api_views.CountryMobileCodesModelAPIView.as_view(),
        name="CountryMobileCodesModelAPIView",
    ),
]
