from rest_framework import generics, filters, permissions
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
)
from user_config.accounts.api.v1.user_management.serializers import (
    UserManagementUserCreateModelSerializer,
    UserManagementUserDetailsModelSerializer,
    UserManagementUserListModelSerializer,
    UserManagementUserReassignmentSerializer,
    UserManagementUserUpdateDetailsModelSerializer,
    UserManagementUserUpdateModelSerializer,
)
from user_config.accounts.api.v1.utils.constants import (
    REUSER_ASSIGNMENT_SUCCESS_MESSAGE,
)
from user_config.accounts.api.v1.utils.queryset.user_management_table_filter_queryset import (
    user_management_table_filter_queryset,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from user_config.user_auth.models import UserModel


class UserManagementUserGenericAPIView(
    CoreGenericPutAPIView, CoreGenericListCreateAPIView, generics.ListCreateAPIView
):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["username", "email", "login_id", "user_role__title"]

    def get_queryset(self):
        return user_management_table_filter_queryset(
            queryset=self.queryset.all(),
            user_instance=self.request.user,
            params=self.request.GET.dict(),
        )

    def get_serializer_class(self):

        return {
            "GET": UserManagementUserListModelSerializer,
            "POST": UserManagementUserCreateModelSerializer,
            "PUT": UserManagementUserUpdateModelSerializer,
        }.get(self.request.method)


class UserManagementUserDetailsGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False
    pk_scope = "KWARGS"

    def get_serializer_class(self):
        return {
            "GET": UserManagementUserDetailsModelSerializer,
        }.get(self.request.method)


class UserManagementUserUpdateDetailsGenericAPIView(
    CoreGenericGetAPIView, generics.GenericAPIView
):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False
    pk_scope = "KWARGS"

    def get_serializer_class(self):

        return {
            "GET": UserManagementUserUpdateDetailsModelSerializer,
        }.get(self.request.method)


class UserManagementAssignmentAPIView(CoreGenericPutAPIView, generics.GenericAPIView):
    queryset = UserModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    many = False
    pk_scope = "KWARGS"
    success_message = REUSER_ASSIGNMENT_SUCCESS_MESSAGE

    def get_serializer_class(self):
        return {
            "PUT": UserManagementUserReassignmentSerializer,
        }.get(self.request.method)
