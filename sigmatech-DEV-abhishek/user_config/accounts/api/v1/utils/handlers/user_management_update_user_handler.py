from typing import List, Tuple, Callable, Optional
from django.db import transaction
from django.db.models.query import QuerySet

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.format_validator import is_format_validator_email
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.accounts.models import UserAssignedProdudctsModel, UserDetailModel
from core_utils.utils.enums import CoreUtilsStatusEnum
from user_config.accounts.api.v1.utils.constants import (
    ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE,
    FIELD_REQUIRED_ERROR_MESSAGE,
    INCORRECT_AREA_ID_ERROR_MESSAGE,
    INCORRECT_CITY_ID_ERROR_MESSAGE,
    INCORRECT_PINCODE_ID_ERROR_MESSAGE,
    INCORRECT_REGION_ID_ERROR_MESSAGE,
    INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE,
    INCORRECT_ZONE_ID_ERROR_MESSAGE,
    REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE,
    REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE,
    USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE,
    USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT,
    USER_ROLE_INCORRECT_ERROR_MESSAGE,
)
from user_config.accounts.api.v1.utils.handlers.user_management_create_user_handler import (
    USER_UNIQUE_AND_REQUIRED_FIELD,
)
from user_config.accounts.api.v1.utils.queryset.region_hierarchal_queryset import (
    get_user_assigned_area_queryset,
    get_user_assigned_city_queryset,
    get_user_assigned_pincode_queryset,
    get_user_assigned_region_queryset,
    get_user_assigned_zone_queryset,
)
from user_config.accounts.api.v1.utils.role_based_utils import (
    has_user_permission_to_role,
    list_of_user_id_under_user_instance,
)
from user_config.accounts.models import UserDetailModel
from user_config.user_auth.models import UserModel, UserRoleModel
from user_config.user_auth.enums import UserRoleEnum
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INVALID_STATUS_ERROR_MESSAGE,
)

from store.configurations.loan_config.models import LoanConfigurationsProductAssignmentModel

class UserManagementUpdateUserHandler(CoreGenericBaseHandler):
    _activity_type: str = "CONFIGURATION_USER_MANAGEMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    user_role_instance: Optional[UserRoleModel] = None
    reports_to_instance: Optional[UserModel] = None
    user_instance: Optional[UserModel] = None

    region_instance: Optional[RegionConfigurationRegionModel] = None
    zone_instance: Optional[RegionConfigurationZoneModel] = None

    city_queryset: QuerySet[RegionConfigurationCityModel] = RegionConfigurationCityModel.objects.none()
    pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = RegionConfigurationPincodeModel.objects.none()
    area_queryset: QuerySet[RegionConfigurationAreaModel] = RegionConfigurationAreaModel.objects.none()

    region_payload_id: Optional[str] = None
    zone_payload_id: Optional[str] = None
    city_payload_id: List[str] = []
    pincode_payload_id: List[str] = []
    area_payload_id: List[str] = []

    def set_payload(self) -> None:
        print("got the data ======>", self.data)
        self.region_payload_id = self.data.get("region_id", None)
        self.zone_payload_id = self.data.get("zone_id", None)
        self.city_payload_id = self.data.get("city_id", [])
        self.pincode_payload_id = self.data.get("pincode_id", [])
        self.area_payload_id = self.data.get("area_id", [])
        self.product_assignment_payload = self.data.get("product_assignment_id", [])
        self.unproduct_assignment_payload = self.data.get("unproduct_assignment_id", [])

    def validate(self) -> Optional[Tuple[str, str]]:
        self.set_payload()
        print("payload set .... 1<=====")
        self.logger.debug(f"Starting validation for user update with payload: {self.data}")
        print("id is there .... 2<=====", self.data.get("id"))
        try:
            if not self.data.get("id"):
                return "id", f"id {FIELD_REQUIRED_ERROR_MESSAGE}"
            self.user_instance = self.queryset.get(pk=self.data.get("id"))
        except UserModel.DoesNotExist:
            return "id", "User does not exist"

        if self.is_status_update_method():
            if not self.valid_status_enum():
                return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")
            return None

        validation_methods: List[Callable[[], Tuple[Optional[str], Optional[str]]]] = [
            self.check_user_details_unique_and_required,
            self.validate_region_level_fields,
        ]

        for method in validation_methods:
            field, error = method()
            if field:
                self.logger.warning("Validation failed at %s: %s", field, error)
                return self.set_error_message(error_message=error, key=field)

        self.logger.info(f"All validations passed successfully for user update: {self.data.get('username')}")
        return None

    def check_user_details_unique_and_required(self) -> Tuple[Optional[str], Optional[str]]:
        self.logger.debug(f"Validating unique and optional user details for: {self.data.get('username')}")
        for field in USER_UNIQUE_AND_REQUIRED_FIELD:
            field_value = self.data.get(field["field"])
            if field_value and self.queryset.filter(**{field["field"]: field_value}).exclude(pk=self.user_instance.pk).exists():
                return field["field"], field["error_message"]

        if self.data.get("email") and not is_format_validator_email(email=self.data["email"]):
            return "email", USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT

        if self.queryset.filter(reports_to=self.user_instance).exists():
            for key in USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE.keys():
                if self.data.get(key):
                    return key, USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE[key]

        if self.data.get("user_role"):
            print("role is there", self.data.get("user_role"))
            try:
                print("role is there 2", self.data.get("user_role"))
                self.user_role_instance = UserRoleModel.objects.get(pk=self.data["user_role"])
            except (KeyError, UserRoleModel.DoesNotExist):
                return "user_role", USER_ROLE_INCORRECT_ERROR_MESSAGE

            if self.user_role_instance.role == UserRoleEnum.ADMIN.value:
                return "user_role", ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE

            if not has_user_permission_to_role(self.request.user, self.user_role_instance):
                return "user_role", REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE
        else:
            self.user_role_instance = self.user_instance.user_role

        if self.data.get("reports_to"):
            try:
                self.reports_to_instance = self.queryset.get(pk=self.data["reports_to"])
            except UserModel.DoesNotExist:
                return "reports_to", INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE

            sub_ordinate_user_ids = list_of_user_id_under_user_instance(self.request.user)
            if str(self.reports_to_instance.pk) not in sub_ordinate_user_ids:
                return "reports_to", REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE
        elif self.user_role_instance.role != UserRoleEnum.SR_MANAGER.value:
            self.reports_to_instance = self.user_instance.reports_to
            if not self.reports_to_instance:
                return "reports_to", f"reports_to {FIELD_REQUIRED_ERROR_MESSAGE}"

        self.logger.info("Unique and optional user detail validation passed")
        return None, None

    def validate_region_level_fields(self) -> Tuple[Optional[str], Optional[str]]:
        self.logger.debug(f"Validating region-level fields for role: {getattr(self.user_role_instance, 'role', None)}")
        print("validrion started ....")
        try:
            user_instance: UserModel = self.queryset.get(pk=self.data.get("id"))
        except UserModel.DoesNotExist:
            return "id", "User does not exist"
        user_detail_instance: UserDetailModel = UserDetailModel.objects.get(user=user_instance)

        if "city_id" not in self.data and ("pincode_id" in self.data or "area_id" in self.data):
            self.city_payload_id = list(user_detail_instance.assigned_city.values_list("pk", flat=True))
        if "pincode_id" not in self.data and "area_id" in self.data:
            self.pincode_payload_id = list(user_detail_instance.assigned_pincode.values_list("pk", flat=True))

        if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
            if self.region_payload_id:
                try:
                    self.region_instance: RegionConfigurationRegionModel = (
                        get_user_assigned_region_queryset(user_instance=self.request.user).get(pk=self.region_payload_id)
                    )
                    self.logger.info("Validated Region ID: %s", self.region_payload_id)
                except RegionConfigurationRegionModel.DoesNotExist:
                    return "region_id", INCORRECT_REGION_ID_ERROR_MESSAGE

        if self.user_role_instance.role == UserRoleEnum.MANAGER.value:
            if self.zone_payload_id:
                try:
                    self.zone_instance: RegionConfigurationZoneModel = (
                        get_user_assigned_zone_queryset(user_instance=self.reports_to_instance or user_instance.reports_to).get(pk=self.zone_payload_id)
                    )
                    self.logger.info(f"Validated Zone ID: {self.zone_payload_id}")
                except RegionConfigurationZoneModel.DoesNotExist:
                    return "zone_id", INCORRECT_ZONE_ID_ERROR_MESSAGE
            elif not user_detail_instance.assigned_zone.exists():
                return "zone_id", FIELD_REQUIRED_ERROR_MESSAGE

        if user_instance.reports_to and ((self.reports_to_instance or user_instance.reports_to).user_role.role == UserRoleEnum.FIELD_OFFICER.value):
            if self.city_payload_id or self.pincode_payload_id:
                error_field: str = "city_id" if self.city_payload_id else "pincode_id"
                return error_field, f"{error_field} {FIELD_REQUIRED_ERROR_MESSAGE}"

        if user_instance.reports_to and ((self.reports_to_instance or user_instance.reports_to).user_role.role == UserRoleEnum.SUPERVISOR.value):
            if self.pincode_payload_id and not self.city_payload_id:
                return "city_id", f"city_id {FIELD_REQUIRED_ERROR_MESSAGE}"

        if self.city_payload_id:
            self.city_queryset: QuerySet[RegionConfigurationCityModel] = (
                get_user_assigned_city_queryset(user_instance=self.reports_to_instance or user_instance.reports_to)
                .filter(pk__in=self.city_payload_id)
            )
            if self.city_queryset.count() != len(self.city_payload_id):
                return "city_id", INCORRECT_CITY_ID_ERROR_MESSAGE

        if self.pincode_payload_id:
            self.pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
                get_user_assigned_pincode_queryset(user_instance=self.reports_to_instance or user_instance.reports_to, city=self.city_payload_id)
                .filter(pk__in=self.pincode_payload_id)
            )
            if self.pincode_queryset.count() != len(self.pincode_payload_id):
                return "pincode_id", INCORRECT_PINCODE_ID_ERROR_MESSAGE

        if self.area_payload_id:
            self.area_queryset: QuerySet[RegionConfigurationAreaModel] = (
                get_user_assigned_area_queryset(user_instance=self.reports_to_instance or user_instance.reports_to, pincode=self.pincode_payload_id)
                .filter(pk__in=self.area_payload_id)
            )
            if self.area_queryset.count() != len(self.area_payload_id):
                return "area_id", INCORRECT_AREA_ID_ERROR_MESSAGE

        self.logger.info("Region-level field validation passed for user")
        return None, None

    def create(self) -> Optional[UserModel]:
        print("update is running ....")
        self.logger.info(f"Starting user update for user ID: {self.data.get('id')}")

        role_changed: bool = self.data.get("user_role") and str(self.user_instance.user_role.pk) != self.data["user_role"]
        reports_to_changed: bool = self.data.get("reports_to") and (not self.user_instance.reports_to or str(self.user_instance.reports_to.pk) != self.data["reports_to"])

        with transaction.atomic():
            if self.is_status_update_method():
                self.user_instance.status = self.data["status"]
                self.user_instance.save()
                self.set_toast_message_value(value=self.user_instance.username)
                self.update_core_generic_updated_by(instance=self.user_instance, log_activity=True)
                self.logger.info(f"User status update successfully for: {self.user_instance.username}")
                return self.user_instance

            if self.data.get("username"):
                self.user_instance.username = self.data["username"]
            if self.data.get("login_id"):
                self.user_instance.login_id = self.data["login_id"]
            if self.data.get("email"):
                self.user_instance.email = self.data["email"]
            if self.data.get("phone_number"):
                self.user_instance.phone_number = self.data["phone_number"]
            if self.data.get("user_role"):
                self.user_instance.user_role = self.user_role_instance
            if self.data.get("reports_to"):
                self.user_instance.reports_to = self.reports_to_instance

            user_detail_instance: UserDetailModel = UserDetailModel.objects.get(user=self.user_instance)
            if self.data.get("profile_picture"):
                user_detail_instance.profile_picture = self.data["profile_picture"]

            if role_changed or reports_to_changed:
                self.logger.info(f"{'Role' if role_changed else 'Reports_to'} changed for user {self.user_instance.username}, resetting dependency fields")
                user_detail_instance.assigned_region.clear()
                user_detail_instance.assigned_zone.clear()
                user_detail_instance.assigned_city.clear()
                user_detail_instance.assigned_pincode.clear()
                user_detail_instance.assigned_area.clear()
                if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
                    self.user_instance.reports_to = None

            if "region_id" in self.data:
                user_detail_instance.assigned_zone.clear()
                user_detail_instance.assigned_city.clear()
                user_detail_instance.assigned_pincode.clear()
                user_detail_instance.assigned_area.clear()
            if "zone_id" in self.data:
                user_detail_instance.assigned_city.clear()
                user_detail_instance.assigned_pincode.clear()
                user_detail_instance.assigned_area.clear()
            if "city_id" in self.data:
                user_detail_instance.assigned_pincode.clear()
                user_detail_instance.assigned_area.clear()
            if "pincode_id" in self.data:
                user_detail_instance.assigned_area.clear()

            if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
                if "region_id" in self.data:
                    user_detail_instance.assigned_region.clear()
                    if self.region_payload_id and self.region_instance:
                        user_detail_instance.assigned_region.set([self.region_instance])
                        self.logger.info(f"Assigned Region: {self.region_payload_id}")
            elif self.user_role_instance.role == UserRoleEnum.MANAGER.value:
                if "zone_id" in self.data:
                    user_detail_instance.assigned_zone.clear()
                    if self.zone_payload_id and self.zone_instance:
                        user_detail_instance.assigned_zone.set([self.zone_instance])
                        self.logger.info(f"Assigned Zone: {self.zone_instance.pk}")
            elif self.user_role_instance.role in [UserRoleEnum.SUPERVISOR.value, UserRoleEnum.FIELD_OFFICER.value]:
                if "city_id" in self.data:
                    user_detail_instance.assigned_city.clear()
                    if self.city_queryset.exists():
                        user_detail_instance.assigned_city.set(self.city_queryset)
                        self.logger.info(f"Assigned Cities: {list(self.city_queryset.values_list('pk', flat=True))}")
                if "pincode_id" in self.data:
                    user_detail_instance.assigned_pincode.clear()
                    if self.pincode_queryset.exists():
                        user_detail_instance.assigned_pincode.set(self.pincode_queryset)
                        self.logger.info(f"Assigned Pincodes: {list(self.pincode_queryset.values_list('pk', flat=True))}")
                if "area_id" in self.data:
                    user_detail_instance.assigned_area.clear()
                    if self.area_queryset.exists():
                        user_detail_instance.assigned_area.set(self.area_queryset)
                        self.logger.info(f"Assigned Areas: {list(self.area_queryset.values_list('pk', flat=True))}")


            # assigned_products_payload and unassigned_products_payload handling can be added here if needed
            print("======================================>",self.product_assignment_payload,"<=========  =========================")
            if self.product_assignment_payload:
                valid_product_ids= LoanConfigurationsProductAssignmentModel.objects.filter(
                    pk__in=self.product_assignment_payload, 
                )
                for product in valid_product_ids:
                    obj, create = UserAssignedProdudctsModel.objects.get_or_create(
                        user=self.user_instance,
                        product_assignment= product,
                        defaults={
                            "status": CoreUtilsStatusEnum.ACTIVATED.value,}
                    )
                    if not create and obj.status != CoreUtilsStatusEnum.ACTIVATED.value:
                        obj.status = CoreUtilsStatusEnum.ACTIVATED.value
                        obj.save()
                    
                    print(f"Product assigned: {obj.product_assignment} | User: {obj.user} | Status: {obj.status} | Created: {create}")

            if self.unproduct_assignment_payload:
                updatedcount=UserAssignedProdudctsModel.objects.filter(
                    user = self.user_instance,
                    product_assignment__in=self.unproduct_assignment_payload
                ).update(status=CoreUtilsStatusEnum.DEACTIVATED.value)

                print(f"Products unassigned count: {updatedcount} ")

                deactive_products= UserAssignedProdudctsModel.objects.filter(
                    
                    user = self.user_instance,
                    product_assignment__in=self.unproduct_assignment_payload,
                )

                for prod in deactive_products:
                    print(f"------------------>Product: {prod.product_assignment}, Status: {prod.status}")

            print("saving user ======>", self.user_instance)
            self.user_instance.save()
            user_detail_instance.save()

        self.set_toast_message_value(value=self.user_instance.username)
        self.update_core_generic_updated_by(instance=self.user_instance, log_activity=True)
        self.logger.info(f"User update completed successfully for: {self.user_instance.username}")
        return self.user_instance
