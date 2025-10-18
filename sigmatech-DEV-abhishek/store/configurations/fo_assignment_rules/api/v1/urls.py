from django.urls import path
from store.configurations.loan_config.api.v1.generics import views as generic_views
from typing import List
from store.configurations.fo_assignment_rules.api.v1.generics import (
    views as generic_views,
)
from store.configurations.fo_assignment_rules.api.v1.generics import (
    views as generic_views,
)
from store.configurations.fo_assignment_rules.api.v1.helper_apis import (
    views as helper_list_views,
)

generic_urlpatterns: List = [
    path(
        "fo-assignment-api/",
        generic_views.ConfigurationFOAssignmentRulesAPIView.as_view(),
        name="RegionConfigurationRegionGenericAPIView",
    ),
    path(
        "fo-assignment-reset-api/",
        generic_views.ConfigurationFOAssignmentRuleResetAPIView.as_view(),
        name="RegionConfigurationRegionGenericAPIView",
    ),
]

helper_list_urlpatterns: List = [
    path(
        "fo-assignment-user-list-helper/",
        helper_list_views.FOAssignementUserHelperGenericAPIView.as_view(),
        name="RegionConfigurationRegionHelperGenericAPIView",
    ),
    path(
        "fo-assignment-zone-list-helper/",
        helper_list_views.FOAssignementZoneHelperGenericAPIView.as_view(),
        name="RegionConfigurationRegionHelperGenericAPIView",
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
