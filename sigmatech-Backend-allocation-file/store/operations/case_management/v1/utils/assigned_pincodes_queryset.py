from store.operations.case_management.models import CaseManagementCaseModel
from user_config.accounts.api.v1.utils.user_reports_hierarichal_list import (
    get_descendant_users,
)
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.models import UserModel
from django.db.models.query import QuerySet
from typing import List, Optional


def get_all_pincodes_under_fo(user_queryset: QuerySet[UserModel]) -> List[str]:

    assigned_pincodes_pk_list: List[str] = []
    for user_instance in user_queryset:
        assigned_pincodes_pk_list.extend(
            user_instance.UserDetailModel_user.assigned_pincode.values_list(
                "pk", flat=True
            )
        )
    return assigned_pincodes_pk_list


def case_management_filter_queryset(
    queryset: QuerySet[CaseManagementCaseModel], user_instance: UserModel
):
    descendant_users: List[UserModel] = get_descendant_users(
        user_instance=user_instance
    )

    assigned_pincode_list: Optional[List[str]] = []
    for query in descendant_users:
        if query.user_role.role == UserRoleEnum.FIELD_OFFICER.value:
            assigned_pincode_list.extend(
                query.UserDetailModel_user.assigned_pincode.values_list("pk", flat=True)
            )

    result = queryset.filter(residential_pin_code__pk__in=assigned_pincode_list)
    return result
