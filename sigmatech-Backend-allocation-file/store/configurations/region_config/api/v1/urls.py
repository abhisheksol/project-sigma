from django.urls import path
from store.configurations.loan_config.api.v1.generics import views as generic_views
from typing import List
from store.configurations.region_config.api.v1.helper_apis import (
    views as helper_list_views,
)
from store.configurations.region_config.api.v1.generics import views as generic_views


generic_urlpatterns: List = [
    path(
        "regions-api/",
        generic_views.RegionConfigurationRegionGenericAPIView.as_view(),
        name="RegionConfigurationRegionGenericAPIView",
    ),
    path(
        "zones-api/",
        generic_views.RegionConfigurationZoneGenericAPIView.as_view(),
        name="RegionConfigurationZoneGenericAPIView",
    ),
    path(
        "cities-api/",
        generic_views.RegionConfigurationCityGenericAPIView.as_view(),
        name="RegionConfigurationCityGenericAPIView",
    ),
    path(
        "pincode-api/",
        generic_views.RegionConfigurationPincodeGenericAPIView.as_view(),
        name="RegionConfigurationPincodeGenericAPIView",
    ),
    path(
        "area-api/",
        generic_views.RegionConfigurationAreaGenericAPIView.as_view(),
        name="RegionConfigurationAreaGenericAPIView",
    ),
]

helper_list_urlpatterns: List = [
    path(
        "region-configuration-region-helper-list-api/",
        helper_list_views.RegionConfigurationRegionHelperGenericAPIView.as_view(),
        name="Region-configurationRegionHelperGenericAPIView",
    ),
    path(
        "region-configuration-zone-helper-list-api/",
        helper_list_views.RegionConfigurationZoneHelperGenericAPIView.as_view(),
        name="Region-configurationZoneHelperGenericAPIView",
    ),
    path(
        "region-configuration-all-city-helper-list-api/",
        helper_list_views.RegionConfigurationAllCityHelperGenericAPIView.as_view(),
        name="Region-configurationCityHelperGenericAPIView",
    ),
    path(
        "region-configuration-city-helper-list-api/",
        helper_list_views.RegionConfigurationCityHelperGenericAPIView.as_view(),
        name="Region-configurationCityHelperGenericAPIView",
    ),
    path(
        "region-configuration-pincode-helper-list-api/",
        helper_list_views.RegionConfigurationPincodeHelperGenericAPIView.as_view(),
        name="Region-configurationPincodeHelperGenericAPIView",
    ),
    path(
        "region-configuration-area-helper-list-api/",
        helper_list_views.RegionConfigurationAreaHelperGenericAPIView.as_view(),
        name="Region-configurationAreaHelperGenericAPIView",
    ),
    path(
        "region-configuration-allpincode-helper-list-api/",
        helper_list_views.RegionConfigurationPincodeRangeHelperGenericAPIView.as_view(),
        name="Region-configurationAllPincodeHelperGenericAPIView",
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
