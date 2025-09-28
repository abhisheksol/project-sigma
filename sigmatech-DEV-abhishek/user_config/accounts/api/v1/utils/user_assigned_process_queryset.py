

from store.configurations.loan_config.models import LoanConfigurationsProductAssignmentModel
from django.db.models.query import QuerySet

from user_config.user_auth.models import UserModel

from core_utils.utils.enums import CoreUtilsStatusEnum
def get_reporting_user_assigned_product_assignment_instance(
        queryset: QuerySet[LoanConfigurationsProductAssignmentModel],
        user_id: str) -> QuerySet[LoanConfigurationsProductAssignmentModel]:
    user_instance: UserModel = UserModel.objects.get(pk=user_id)
    if not user_instance.user_role:
        return queryset.all()

    return queryset.filter(
        UserAssignedProdudctsModel_product_assignment__user=user_instance.reports_to
    )


# if parent is assigend to any product then child can see only those products



# def get_reporting_user_assigned_product_assignment_instance(
#     queryset: QuerySet[LoanConfigurationsProductAssignmentModel], user_id: str
# ) -> QuerySet[LoanConfigurationsProductAssignmentModel]:
#     user_instance: UserModel = UserModel.objects.get(pk=user_id)
#     if not user_instance.user_role:
#         return queryset.all()

#     return queryset.filter(
        # pk__in=user_instance.UserAssignedProdudctsModel_user.all()
#         .filter(status=CoreUtilsStatusEnum.ACTIVATED.value)
#         .values_list("product_assignment", flat=True)
#     )
