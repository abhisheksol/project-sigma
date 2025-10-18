from core_utils.utils.enums import CoreUtilsStatusEnum
from core_utils.utils.global_variables import STATUS_ACTIVATED_GLOBAL_FILTERSET
from user_config.accounts.models import UserDetailModel
from store.operations.case_management.models import CaseManagementCaseAddressModel
from django.db.models import Q
from store.configurations.region_config.models import RegionConfigurationZoneModel


def validate_status_change(instance, old_status, new_status, user_qs):
    if old_status == new_status:
        return None

    if new_status == CoreUtilsStatusEnum.DEACTIVATED.value:
        if user_qs.filter(status=CoreUtilsStatusEnum.ACTIVATED.value).exists():
            return f"Cannot deactivate {instance.__class__.__name__} while users are active."
    return None


def can_edit_region(instance):
    if instance.status == CoreUtilsStatusEnum.DEACTIVATED.value:
        return False

    if (
        UserDetailModel.objects.filter(
            Q(assigned_region=instance)
            | Q(assigned_zone__region=instance)
            | Q(assigned_city__zone__region=instance)
            | Q(assigned_pincode__city__zone__region=instance)
            | Q(assigned_area__pincode__city__zone__region=instance)
        )
        .filter(**STATUS_ACTIVATED_GLOBAL_FILTERSET)
        .exists()
    ):
        return "Cannot update region: active users exist."

    if (
        CaseManagementCaseAddressModel.objects.filter(
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .filter(
            Q(pin_code__city__zone__region=instance)
            | Q(region_config_city__zone__region=instance)
        )
        .exists()
    ):
        return "Cannot update region: active cases exist."

    return False


def can_edit_zone(instance: RegionConfigurationZoneModel):

    if instance.status == CoreUtilsStatusEnum.DEACTIVATED.value:
        return False

    print("running...")

    if (
        UserDetailModel.objects.filter(
            Q(assigned_zone=instance)
            | Q(assigned_city__zone=instance)
            | Q(assigned_pincode__city__zone=instance)
            | Q(assigned_area__pincode__city__zone=instance)
        )
        .filter(
            # **STATUS_ACTIVATED_GLOBAL_FILTERSET
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .exists()
    ):
        return f"Cannot update zone: active users exist."

    if (
        CaseManagementCaseAddressModel.objects.filter(
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .filter(Q(pin_code__city__zone=instance) | Q(region_config_city__zone=instance))
        .exists()
    ):
        return "Cannot update zone: active cases exist."

    return False


# =========================== check city ===========================


def can_edit_city(instance):
    if instance.status == CoreUtilsStatusEnum.DEACTIVATED.value:
        return False

    if (
        UserDetailModel.objects.filter(
            Q(assigned_city=instance)
            | Q(assigned_pincode__city=instance)
            | Q(assigned_area__pincode__city=instance)
        )
        .filter(
            # **STATUS_ACTIVATED_GLOBAL_FILTERSET
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .exists()
    ):
        return f"Cannot update city: active users exist."

    if (
        CaseManagementCaseAddressModel.objects.filter(
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .filter(Q(pin_code__city=instance))
        .exists()
    ):
        return "Cannot update city: active cases exist."

    return False


# =========================== check pincode ===========================


def can_edit_pincode(instance):
    if instance.status == CoreUtilsStatusEnum.DEACTIVATED.value:
        return False

    if (
        UserDetailModel.objects.filter(
            Q(assigned_pincode=instance) | Q(assigned_area__pincode=instance)
        )
        .filter(
            # **STATUS_ACTIVATED_GLOBAL_FILTERSET
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .exists()
    ):
        return f"Cannot update pincode: active users exist."

    if (
        CaseManagementCaseAddressModel.objects.filter(
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .filter(Q(pin_code=instance))
        .exists()
    ):
        return "Cannot update pincode: active cases exist."

    return False


# =========================== check area ===========================


def can_edit_area(instance):
    if instance.status == CoreUtilsStatusEnum.DEACTIVATED.value:
        return False

    if (
        UserDetailModel.objects.filter(Q(assigned_area=instance))
        .filter(
            # **STATUS_ACTIVATED_GLOBAL_FILTERSET
            status=CoreUtilsStatusEnum.ACTIVATED.value
        )
        .exists()
    ):
        return f"Cannot update area: active users exist."

    # if CaseManagementCaseAddressModel.objects.filter(
    #     status=CoreUtilsStatusEnum.ACTIVATED.value
    # ).filter(
    #     Q(pin_code__area=instance)
    # ).exists():
    #     return "Cannot update area: active cases exist."

    return False
