from django.urls import path

from user_config.accounts.api.v1.helper_apis import views as helper_list_views
from user_config.accounts.api.v1.user_management import views as user_management_views

helper_list_urlpattern: list = [
    path(
        "user-role-hierarchal-helper-list-api/",
        helper_list_views.UserRoleHelperListAPIView.as_view(),
        name="UserRoleHelperListAPIView",
    ),
    path(
        "user-reports-to-hierarchal-helper-list-api/",
        helper_list_views.UserReportsToHelperListAPIView.as_view(),
        name="UserReportsToHelperListAPIView",
    ),
    path(
        "user-assigned-region-hierarchal-helper-list-api/",
        helper_list_views.UserManagementUserRegionHelperListAPIView.as_view(),
        name="UserManagementUserRegionHelperListAPIView",
    ),
    path(
        "user-assigned-zone-hierarchal-helper-list-api/",
        helper_list_views.UserManagementUserZoneHelperListAPIView.as_view(),
        name="UserManagementUserZoneHelperListAPIView",
    ),
    path(
        "user-assigned-city-hierarchal-helper-list-api/",
        helper_list_views.UserManagementUserCityHelperListAPIView.as_view(),
        name="UserManagementUserCityHelperListAPIView",
    ),
    path(
        "user-assigned-pincode-hierarchal-helper-list-api/",
        helper_list_views.UserManagementUserPincodeHelperListAPIView.as_view(),
        name="UserManagementUserPincodeHelperListAPIView",
    ),
    path(
        "user-assigned-area-hierarchal-helper-list-api/",
        helper_list_views.UserManagementUserAreaHelperListAPIView.as_view(),
        name="UserManagementUserAreaHelperListAPIView",
    ),
    path(
        "region-configuration-user-assigned-products-helper-list-api/",
        helper_list_views.ProductAssignmentHelperAPIView.as_view(),
        name="Region-configurationUserAssignedProductsHelperGenericAPIView",
    ),
]

user_management_urlpatterns: list = [
    path(
        "user-management-api/",
        user_management_views.UserManagementUserGenericAPIView.as_view(),
        name="UserManagementUserGenericAPIView",
    ),
    path(
        "user-management-api/<str:id>/",
        user_management_views.UserManagementUserDetailsGenericAPIView.as_view(),
        name="UserManagementUserDetailsGenericAPIView",
    ),
    path(
        "user-management-update-detail-api/<str:id>/",
        user_management_views.UserManagementUserUpdateDetailsGenericAPIView.as_view(),
        name="UserManagementUserUpdateDetailsGenericAPIView",
    ),
    path(
        "user-re-assignment-api/",
        user_management_views.UserManagementAssignmentAPIView.as_view(),
        name="UserManagementAssignmentAPIView",
    ),
]

urlpatterns: list = [*helper_list_urlpattern, *user_management_urlpatterns]
