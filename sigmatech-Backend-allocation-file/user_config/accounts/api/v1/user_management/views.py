from rest_framework import generics, filters, permissions
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
)
from user_config.accounts.api.v1.user_management.serializers import (
    EligibleFOListByCaseSerializer,
    FoAssignmentSerializer,
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







from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from django.db.models.query import QuerySet
 
from user_config.user_auth.models import UserModel
from core_utils.utils.enums import CoreUtilsStatusEnum
from user_config.accounts.models import UserDetailModel
from store.operations.case_management.models import CaseManagementCaseModel
 
from django.db.models import Q
 
 
def get_reporting_user_assigned_product_assignment_instance(
    queryset: QuerySet[LoanConfigurationsProductAssignmentModel], user_id: str
) -> QuerySet[LoanConfigurationsProductAssignmentModel]:
    user_instance: UserModel = UserModel.objects.get(pk=user_id)
    if not user_instance.user_role:
        return queryset.all()
 
    return queryset.filter(
        pk__in=user_instance.UserAssignedProdudctsModel_user.all()
        .filter(status=CoreUtilsStatusEnum.ACTIVATED.value)
        .values_list("product_assignment", flat=True)
    )
 
 
def get_Fo_user_assigned_case_queryset(
    case_id: str,
    queryset: QuerySet[UserDetailModel] = UserDetailModel.objects.all(),
) -> QuerySet[UserDetailModel]:
    """
    Returns a queryset of FO (Field Officer) users assigned to a case based on
    the case's residential pin code and area.
 
    The logic is as follows:
    1. Fetch the CaseManagementCaseModel instance using the provided `case_id`.
       If it does not exist, return an empty queryset.
    2. If the case has both `residential_pin_code` and `residential_sub_area`:
       - Return FO users assigned to the same pin code and same sub-area, OR
       - Assigned to the same pin code but with no specific sub-area.
       (This allows fallback to pin code only when sub-area is not defined for FO.)
    3. If the case has only `residential_pin_code`, return FO users assigned to that pin code.
    4. If neither is defined, return an empty queryset.
 
    Args:
        case_id (str): UUID of the CaseManagementCaseModel instance.
        queryset (QuerySet, optional): Base queryset of UserDetailModel to filter from.
            Defaults to all UserDetailModel objects.
 
    Returns:
        QuerySet[UserDetailModel]: Filtered queryset of FO users for the case.
    """
    try:
        # Fetch the case with related residential pin code and area for efficient querying
        case_instance: CaseManagementCaseModel = CaseManagementCaseModel.objects.select_related(
            "residential_pin_code",
            "residential_sub_area"
        ).get(id=case_id)
    except CaseManagementCaseModel.DoesNotExist:
        # If the case does not exist, return empty queryset
        return queryset.none()
 
    # Debug prints (can remove in production)
    print("case residential_pin_code ---->",
          case_instance.residential_pin_code)
    print("case residential_sub_area ---->",
          case_instance.residential_sub_area)
 
    # Case has both pin code and sub-area
    if case_instance.residential_pin_code and case_instance.residential_sub_area:
        return UserDetailModel.objects.filter(
            # FO assigned to both the same pin code AND the same sub-area
            Q(assigned_pincode=case_instance.residential_pin_code) &
            Q(assigned_area=case_instance.residential_sub_area) |
            # OR FO assigned to same pin code but no specific sub-area
            Q(assigned_pincode=case_instance.residential_pin_code) &
            Q(assigned_area__isnull=True)
            # TODO: Consider handling cases where FO sub-area is empty separately
        ).select_related("user")
 
    # Case has only pin code defined
    elif case_instance.residential_pin_code:
        return queryset.filter(
            assigned_pincode=case_instance.residential_pin_code
        )
 
    # Neither pin code nor sub-area is defined
    return queryset.none()

class EligibleFOListByCaseGenericAPIView(
    CoreGenericGetAPIView,
    generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserDetailModel.objects.all().filter(
        user__user_role__role="FIELD_OFFICER",
    )
 
    def get_queryset(self):
 
        case_id = self.request.query_params.get("case_id")
 
        print("case_id---->", case_id)
 
        if case_id:
            return get_Fo_user_assigned_case_queryset(case_id, self.queryset)
 
    def get_serializer_class(self):
        return {
            "GET": EligibleFOListByCaseSerializer,
        }.get(self.request.method)
    



class FOAssignCaseAPIView(CoreGenericPutAPIView,
                           generics.GenericAPIView, CoreGenericListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CaseManagementCaseModel.objects.all()

    def get_serializer_class(self):
        return {
            "PUT": FoAssignmentSerializer,
        }.get(self.request.method)
