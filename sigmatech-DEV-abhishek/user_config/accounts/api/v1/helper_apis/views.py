"""
API views for retrieving hierarchical location data and user role/reporting information.

This module defines a set of Django REST Framework API views for accessing user roles, reporting
hierarchies, and location-based querysets (regions, zones, cities, pincodes, areas). Each view
leverages role-based access control to filter data based on the authenticated user's permissions
and optional query parameters (e.g., user_id, region, city, pincode).
"""

from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from user_config.accounts.api.v1.utils.queryset.region_hierarchal_queryset import (
    get_user_assigned_area_queryset,
    get_user_assigned_city_queryset,
    get_user_assigned_pincode_queryset,
    get_user_assigned_region_queryset,
    get_user_assigned_zone_queryset,
)
from user_config.accounts.api.v1.utils.queryset.user_reports_to_queryset import (
    get_user_reports_queryset,
)
from user_config.accounts.api.v1.utils.user_assigned_process_queryset import (
    get_reporting_user_assigned_product_assignment_instance,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetDataFromSerializerAPIView,
    CoreGenericGetAPIView,
)
from user_config.user_auth.models import UserModel
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from .serializers import (
    FolistingHelperSerializer,
    ProductAssignmentHelperSerializer,
    UserManagementUserAreaHelperListModelSerializer,
    UserManagementUserCityHelperListModelSerializer,
    UserManagementUserPincodeHelperListModelSerializer,
    UserManagementUserRegionHelperListModelSerializer,
    UserManagementUserZoneHelperListModelSerializer,
    UserReportsToHelperListModelSerializer,
    UserRoleHelperListSerializer,
)
from rest_framework import generics, permissions
from typing import Dict, Optional
from django.db.models.query import QuerySet


class UserRoleHelperListAPIView(
    CoreGenericGetDataFromSerializerAPIView, generics.GenericAPIView
):
    """
    API view to retrieve user role data.

    This view provides a list of user roles available in the system, accessible only
    to authenticated users. It uses the UserRoleHelperListSerializer to serialize the data.

    Attributes:
        authentication_classes: Specifies custom authentication (CustomAuthentication).
        permission_classes: Ensures only authenticated users can access this endpoint.
    """

    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class based on the HTTP method.

        Returns:
            dict: Maps the HTTP method 'GET' to UserRoleHelperListSerializer.
        """
        return {
            "GET": UserRoleHelperListSerializer,
        }.get(self.request.method)


class UserReportsToHelperListAPIView(CoreGenericGetAPIView, generics.GenericAPIView):
    """
    API view to retrieve users who report to the authenticated user or a specified user role.

    This view filters UserModel instances to return users based on their reporting hierarchy
    and an optional user_role query parameter. If no user_role is provided, an empty queryset
    is returned.

    Attributes:
        queryset: Base queryset of all UserModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset based on the user_role query parameter and the authenticated user.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of users who report to the authenticated user
                      or match the specified user_role.
        """
        params: Dict = self.request.GET.dict()

        queryset: QuerySet[UserModel] = get_user_reports_queryset(
            queryset=self.queryset, params=params, request_user=self.request.user
        )
        if queryset.exists():
            return queryset.distinct()
        return queryset.none()

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing the reporting users data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserReportsToHelperListModelSerializer.
        """
        return {
            "GET": UserReportsToHelperListModelSerializer,
        }.get(self.request.method)


class UserManagementUserRegionHelperListAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    """
    API view to retrieve regions assigned to a user.

    This view filters RegionConfigurationRegionModel instances based on the authenticated
    user or a specified user_id. It uses role-based access rules to ensure only authorized
    regions are returned.

    Attributes:
        queryset: Base queryset of all RegionConfigurationRegionModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = RegionConfigurationRegionModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters regions based on the authenticated user or a specified user_id.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of regions assigned to the user.
        """
        params: Dict = self.request.GET.dict()
        return get_user_assigned_region_queryset(
            queryset=self.queryset,
            user_instance=(
                UserModel.objects.get(pk=params.get("user_id"))
                if params.get("user_id")
                else self.request.user
            ),
        )

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing region data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserManagementUserRegionHelperListModelSerializer.
        """
        return {
            "GET": UserManagementUserRegionHelperListModelSerializer,
        }.get(self.request.method)


class UserManagementUserZoneHelperListAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    """
    API view to retrieve zones assigned to a user, optionally filtered by region.

    This view filters RegionConfigurationZoneModel instances based on the authenticated
    user or a specified user_id, with an optional region filter provided via query parameters.

    Attributes:
        queryset: Base queryset of all RegionConfigurationZoneModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = RegionConfigurationZoneModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters zones based on the authenticated user or a specified user_id, with optional region filtering.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of zones assigned to the user, optionally restricted by region.
        """
        params: Dict = self.request.GET.dict()

        return get_user_assigned_zone_queryset(
            queryset=self.queryset,
            region=str(params.get("region")).split(",") if params.get("region") else [],
            user_instance=(
                UserModel.objects.get(pk=params.get("user_id"))
                if params.get("user_id")
                else self.request.user
            ),
        )

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing zone data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserManagementUserZoneHelperListModelSerializer.
        """
        return {
            "GET": UserManagementUserZoneHelperListModelSerializer,
        }.get(self.request.method)


class UserManagementUserCityHelperListAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    """
    API view to retrieve cities assigned to a user.

    This view filters RegionConfigurationCityModel instances based on the authenticated
    user or a specified user_id, applying role-based access rules to ensure only authorized
    cities are returned.

    Attributes:
        queryset: Base queryset of all RegionConfigurationCityModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = RegionConfigurationCityModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters cities based on the authenticated user or a specified user_id.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of cities assigned to the user.
        """
        params: Dict = self.request.GET.dict()
        return get_user_assigned_city_queryset(
            queryset=self.queryset,
            user_instance=(
                UserModel.objects.get(pk=params.get("user_id"))
                if params.get("user_id")
                else self.request.user
            ),
            zone=str(params.get("zone")).split(",") if params.get("zone") else [],
        )

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing city data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserManagementUserCityHelperListModelSerializer.
        """
        return {
            "GET": UserManagementUserCityHelperListModelSerializer,
        }.get(self.request.method)


class UserManagementUserPincodeHelperListAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    """
    API view to retrieve pincodes assigned to a user, optionally filtered by city.

    This view filters RegionConfigurationPincodeModel instances based on the authenticated
    user or a specified user_id, with an optional city filter provided via query parameters.

    Attributes:
        queryset: Base queryset of all RegionConfigurationPincodeModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = RegionConfigurationPincodeModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters pincodes based on the authenticated user or a specified user_id, with optional city filtering.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of pincodes assigned to the user, optionally restricted by city.
        """
        params: Dict = self.request.GET.dict()
        search: Optional[str] = params.get("search")
        search_filter_set: Optional[Dict[str, str]] = {}
        if search:
            search_filter_set: Optional[Dict[str, str]] = {
                "pincode__pincode__icontains": search
            }
        if params.get("city"):
            return get_user_assigned_pincode_queryset(
                queryset=self.queryset,
                city=str(params["city"]).split(","),
                user_instance=(
                    UserModel.objects.get(pk=params.get("user_id"))
                    if params.get("user_id")
                    else self.request.user
                ),
            ).filter(**search_filter_set)
        return self.queryset.all().filter(**search_filter_set)

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing pincode data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserManagementUserPincodeHelperListModelSerializer.
        """
        return {
            "GET": UserManagementUserPincodeHelperListModelSerializer,
        }.get(self.request.method)


class UserManagementUserAreaHelperListAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    """
    API view to retrieve areas assigned to a user, optionally filtered by pincode.

    This view filters RegionConfigurationAreaModel instances based on the authenticated
    user or a specified user_id, with an optional pincode filter provided via query parameters.

    Attributes:
        queryset: Base queryset of all RegionConfigurationAreaModel objects.
        authentication_classes: Uses CustomAuthentication for user verification.
        permission_classes: Restricts access to authenticated users only.
    """

    queryset = RegionConfigurationAreaModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters areas based on the authenticated user or a specified user_id, with optional pincode filtering.

        Args:
            None (uses self.request for query parameters and user).

        Returns:
            QuerySet: Filtered queryset of areas assigned to the user, optionally restricted by pincode.
        """
        params: Dict = self.request.GET.dict()
        search: Optional[str] = params.get("search")
        search_filter_set: Optional[Dict[str, str]] = {}
        if search:
            search_filter_set: Optional[Dict[str, str]] = {"title__icontains": search}
        if params.get("pincode"):
            return get_user_assigned_area_queryset(
                queryset=self.queryset,
                pincode=str(params["pincode"]).split(","),
                user_instance=(
                    UserModel.objects.get(pk=params.get("user_id"))
                    if params.get("user_id")
                    else self.request.user
                ),
            ).filter(**search_filter_set)

        return self.queryset.all().filter(**search_filter_set)

    def get_serializer_class(self):
        """
        Returns the serializer class for serializing area data.

        Returns:
            dict: Maps the HTTP method 'GET' to UserManagementUserAreaHelperListModelSerializer.
        """
        return {
            "GET": UserManagementUserAreaHelperListModelSerializer,
        }.get(self.request.method)


class ProductAssignmentHelperAPIView(CoreGenericGetAPIView, generics.GenericAPIView):
    queryset = LoanConfigurationsProductAssignmentModel.objects.all()

    def get_queryset(self):

        user_id: str = self.request.GET.dict().get("user_id")
        if user_id is None:
            return self.queryset.all()

        return get_reporting_user_assigned_product_assignment_instance(
            queryset=self.queryset, user_id=user_id
        )

    def get_serializer_class(self):
        return {
            "GET": ProductAssignmentHelperSerializer,
        }.get(self.request.method)



class FolistingHelperAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.all()


    def get_serializer_class(self):

        return {
            "GET": FolistingHelperSerializer,
        }.get(self.request.method)