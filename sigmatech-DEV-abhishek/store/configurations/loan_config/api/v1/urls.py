from django.urls import path
from store.configurations.loan_config.api.v1.generics import views as generic_views
from typing import List

from store.configurations.loan_config.api.v1.helper_apis import (
    views as helper_list_views,
)

helper_list_urlpatterns: List = [
    path(
        "process-helper-list-api/",
        helper_list_views.LoanConfigurationsProcessHelperGenericAPIView.as_view(),
        name="LoanConfigurationsProcessHelperGenericAPIView",
    ),
    path(
        "product-helper-list-api/",
        helper_list_views.LoanConfigurationsProductHelperGenericAPIView.as_view(),
        name="LoanConfigurationsProductHelperGenericAPIView",
    ),
    path(
        "monthly-cycle-helper-list-api/",
        helper_list_views.LoanConfigurationsMonthlyCycleHelperGenericAPIView.as_view(),
        name="LoanConfigurationsMonthlyCycleHelperGenericAPIView",
    ),
    path(
        "bucket-helper-list-api/",
        helper_list_views.LoanConfigurationsBucketHelperGenericAPIView.as_view(),
        name="LoanConfigurationsBucketHelperGenericAPIView",
    ),
    path(
        "bucket-range-helper-list-api/",
        helper_list_views.LoanConfigurationsBucketRangeHelperGenericAPIView.as_view(),
        name="LoanConfigurationsBucketRangeHelperGenericAPIView",
    ),
]


generic_urlpatterns: List = [
    path(
        "process-api/",
        generic_views.LoanConfigurationsProcessGenericAPIView.as_view(),
        name="LoanConfigurationsProcessGenericAPIView",
    ),
    path(
        "products-api/",
        generic_views.LoanConfigurationsProductGenericAPIView.as_view(),
        name="LoanConfigurationsProductGenericAPIView",
    ),
    path(
        "monthly-cycles-api/",
        generic_views.LoanConfigurationsMonthlyCycleGenericAPIView.as_view(),
        name="LoanConfigurationsMonthlyCycleGenericAPIView",
    ),
    path(
        "buckets-api/",
        generic_views.LoanConfigurationsBucketGenericAPIView.as_view(),
        name="LoanConfigurationsBucketGenericAPIView",
    ),
    path(
        "bucket-range-api/",
        generic_views.LoanConfigurationsBucketRangeGenericAPIView.as_view(),
        name="LoanConfigurationsBucketRangeGenericAPIView",
    ),
    path(
        "product-assignment-api/",
        generic_views.LoanConfigurationsProductAssignmentGenericAPIView.as_view(),
        name="LoanConfigurationsProductAssignmentGenericAPIView",
    ),
    path(
        "product-assignment-api/<uuid:id>/",
        generic_views.LoanConfigurationsProductDetailGenericAPIView.as_view(),
        name="LoanConfigurationsProductAssignmentGenericAPIView",
    ),
]

urlpatterns: List = [*generic_urlpatterns, *helper_list_urlpatterns]
