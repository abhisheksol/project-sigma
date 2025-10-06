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
from user_config.accounts.api.v1.utils.constants import (
    ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE,
    FIELD_REQUIRED_ERROR_MESSAGE,
    INCORRECT_AREA_ID_ERROR_MESSAGE,
    INCORRECT_CITY_ID_ERROR_MESSAGE,
    INCORRECT_PINCODE_ID_ERROR_MESSAGE,
    INCORRECT_REGION_ID_ERROR_MESSAGE,
    INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE,
    INCORRECT_ZONE_ID_ERROR_MESSAGE,
    INVALID_PRODUCT_ASSIGNMENT_ERROR_KEY,
    INVALID_PRODUCT_ASSIGNMENT_ERROR_MESSAGE,
    INVALID_PRODUCT_UNASSIGNMENT_ERROR_KEY,
    INVALID_PRODUCT_UNASSIGNMENT_ERROR_MESSAGE,
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
from user_config.accounts.models import UserAssignedProdudctsModel, UserDetailModel
from user_config.user_auth.models import UserModel, UserRoleModel
from user_config.user_auth.enums import UserRoleEnum
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INVALID_STATUS_ERROR_MESSAGE,
)
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from core_utils.utils.enums import CoreUtilsStatusEnum
from user_config.accounts.api.v1.utils.user_assigned_process_queryset import (
    get_reporting_user_assigned_product_assignment_instance,
)


class UserManagementUpdateUserHandler(CoreGenericBaseHandler):
    """
    Handler for updating existing users with strict role-based and region-level validations.

    Responsibilities:
    -----------------
    * Validate uniqueness and optional user fields
    * Enforce role restrictions and reporting hierarchy
    * Update region/zone/city/pincode/area mappings conditionally
    * Handle dependency fields (user_role, reports_to, region_id, zone_id, city_id, pincode_id, area_id)
    * Update User and UserDetail records atomically
    * Log every step of validation and update for traceability
    """

    _activity_type: str = "CONFIGURATION_USER_MANAGEMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    # Role and reporting user related instances
    user_role_instance: Optional[UserRoleModel] = None
    reports_to_instance: Optional[UserModel] = None
    user_instance: Optional[UserModel] = None

    # Region hierarchy related instances
    region_instance: Optional[RegionConfigurationRegionModel] = None
    zone_instance: Optional[RegionConfigurationZoneModel] = None

    # Querysets for hierarchical entities
    city_queryset: QuerySet[RegionConfigurationCityModel] = (
        RegionConfigurationCityModel.objects.none()
    )
    pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
        RegionConfigurationPincodeModel.objects.none()
    )
    area_queryset: QuerySet[RegionConfigurationAreaModel] = (
        RegionConfigurationAreaModel.objects.none()
    )

    # Payload IDs
    region_payload_id: Optional[str] = None
    zone_payload_id: Optional[str] = None
    city_payload_id: List[str] = []
    pincode_payload_id: List[str] = []
    area_payload_id: List[str] = []

    def set_payload(self) -> None:
        """
        Extract hierarchical IDs from the request payload for region, zone, city, pincode, and area.

        Sets instance attributes for payload IDs to be used in validation and update processes.
        """
        self.region_payload_id = self.data.get("region_id", None)
        self.zone_payload_id = self.data.get("zone_id", None)
        self.city_payload_id = self.data.get("city_id", [])
        self.pincode_payload_id = self.data.get("pincode_id", [])
        self.area_payload_id = self.data.get("area_id", [])
        self.product_assignment_payload = self.data.get("product_assignment_id", [])
        self.unproduct_assignment_payload = self.data.get("product_unassignment_id", [])

    def validate(self) -> Optional[Tuple[str, str]]:
        """
        Run sequential validations for user update, including user details and region-level fields.

        Logs each validation step and returns the first failure encountered as a tuple of
        (field, error_message). Returns None if all validations pass.

        Returns:
            Optional[Tuple[str, str]]: Field name and error message if validation fails, else None.
        """
        self.set_payload()

        self.logger.debug(
            f"Starting validation for user update with payload: {self.data}"
        )

        try:
            if not self.data.get("id"):
                return "id", f"id {FIELD_REQUIRED_ERROR_MESSAGE}"
            self.user_instance = self.queryset.get(pk=self.data.get("id"))
        except UserModel.DoesNotExist:
            return "id", "User does not exist"

        if self.is_status_update_method():
            if not self.valid_status_enum():
                return self.set_error_message(
                    INVALID_STATUS_ERROR_MESSAGE, key="status"
                )
            return None

        validation_methods: List[Callable[[], Tuple[Optional[str], Optional[str]]]] = [
            self.check_user_details_unique_and_required,
            self.validate_region_level_fields,
            self.validate_process_level_fields,
        ]

        for method in validation_methods:
            field, error = method()
            if field:
                self.logger.warning("Validation failed at %s: %s", field, error)
                return self.set_error_message(error_message=error, key=field)

        self.logger.info(
            f"All validations passed successfully for user update: {self.data.get('username')}"
        )
        return None

    def check_user_details_unique_and_required(
        self,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Validate user’s unique fields, role correctness, and reporting structure.

        Checks for uniqueness of login_id, email, and phone_number if provided, validates email
        format, and enforces role and reporting hierarchy rules. All fields are optional for updates.

        Returns:
            Tuple[Optional[str], Optional[str]]: Field name and error message if validation fails,
            else (None, None).
        """
        self.logger.debug(
            f"Validating unique and optional user details for: {self.data.get('username')}"
        )

        # Check uniqueness for login_id, email, phone_number if provided
        for field in USER_UNIQUE_AND_REQUIRED_FIELD:
            field_value = self.data.get(field["field"])
            if (
                field_value
                and self.queryset.filter(**{field["field"]: field_value})
                .exclude(pk=self.user_instance.pk)
                .exists()
            ):
                return field["field"], field["error_message"]

        # Validate email format if provided
        if self.data.get("email") and not is_format_validator_email(
            email=self.data["email"]
        ):
            return "email", USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT

        # Validate role if provided
        if self.queryset.filter(reports_to=self.user_instance).exists():
            for key in USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE.keys():
                if self.data.get(key):
                    return key, USER_HAS_REPORTING_USERS_DYNAMIC_ERROR_MESSAGE[key]

        if self.data.get("user_role"):
            try:
                self.user_role_instance = UserRoleModel.objects.get(
                    pk=self.data["user_role"]
                )
            except (KeyError, UserRoleModel.DoesNotExist):
                return "user_role", USER_ROLE_INCORRECT_ERROR_MESSAGE

            # Restrict admin role updates
            if self.user_role_instance.role == UserRoleEnum.ADMIN.value:
                return "user_role", ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE

            # Check role update permissions
            if not has_user_permission_to_role(
                self.request.user, self.user_role_instance
            ):
                return (
                    "user_role",
                    REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE,
                )
        else:
            # Use existing role if not provided
            self.user_role_instance = self.user_instance.user_role

        # Validate reporting user if provided
        if self.data.get("reports_to"):
            try:
                self.reports_to_instance = self.queryset.get(pk=self.data["reports_to"])
            except UserModel.DoesNotExist:
                return "reports_to", INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE

            sub_ordinate_user_ids = list_of_user_id_under_user_instance(
                self.request.user
            )
            if str(self.reports_to_instance.pk) not in sub_ordinate_user_ids:
                return "reports_to", REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE
        elif self.user_role_instance.role != UserRoleEnum.SR_MANAGER.value:
            # Use existing reports_to if not provided, but required for non-SR_MANAGER
            self.reports_to_instance = self.user_instance.reports_to
            if not self.reports_to_instance:
                return "reports_to", f"reports_to {FIELD_REQUIRED_ERROR_MESSAGE}"

        self.logger.info("Unique and optional user detail validation passed")
        return None, None

    def validate_region_level_fields(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Validate region, zone, city, pincode, and area assignments based on the user's role
        and reporting manager’s permissions.

        Ensures hierarchical dependencies are respected (e.g., city required for pincodes).
        Sets payload for lower-level fields (city, pincode) if not provided but needed for
        validation of dependent fields.

        Returns:
            Tuple[Optional[str], Optional[str]]: Field name and error message if validation fails,
            else (None, None).
        """
        self.logger.debug(
            f"Validating region-level fields for role: {getattr(self.user_role_instance, 'role', None)}"
        )

        # Fetch the user instance and details being updated
        try:
            user_instance: UserModel = self.queryset.get(pk=self.data.get("id"))
        except UserModel.DoesNotExist:
            return "id", "User does not exist"
        user_detail_instance: UserDetailModel = UserDetailModel.objects.get(
            user=user_instance
        )

        # Set dependency payloads to existing if not provided, for validation of lower levels
        if "city_id" not in self.data and (
            "pincode_id" in self.data or "area_id" in self.data
        ):
            self.city_payload_id = list(
                user_detail_instance.assigned_city.values_list("pk", flat=True)
            )
        if "pincode_id" not in self.data and "area_id" in self.data:
            self.pincode_payload_id = list(
                user_detail_instance.assigned_pincode.values_list("pk", flat=True)
            )

        # Region validation for SR_MANAGER
        if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
            if self.region_payload_id:
                try:
                    self.region_instance: RegionConfigurationRegionModel = (
                        get_user_assigned_region_queryset(
                            user_instance=self.request.user
                        ).get(pk=self.region_payload_id)
                    )
                    self.logger.info("Validated Region ID: %s", self.region_payload_id)
                except RegionConfigurationRegionModel.DoesNotExist:
                    return "region_id", INCORRECT_REGION_ID_ERROR_MESSAGE
            # elif not user_detail_instance.assigned_region.exists():
            #     return "region_id", FIELD_REQUIRED_ERROR_MESSAGE

        # Zone validation for MANAGER
        if self.user_role_instance.role == UserRoleEnum.MANAGER.value:
            if self.zone_payload_id:
                try:
                    self.zone_instance: RegionConfigurationZoneModel = (
                        get_user_assigned_zone_queryset(
                            user_instance=self.reports_to_instance
                            or user_instance.reports_to
                        ).get(pk=self.zone_payload_id)
                    )
                    self.logger.info(f"Validated Zone ID: {self.zone_payload_id}")
                except RegionConfigurationZoneModel.DoesNotExist:
                    return "zone_id", INCORRECT_ZONE_ID_ERROR_MESSAGE
            elif not user_detail_instance.assigned_zone.exists():
                return "zone_id", FIELD_REQUIRED_ERROR_MESSAGE

        # Field Officer restriction
        if user_instance.reports_to and (
            (self.reports_to_instance or user_instance.reports_to).user_role.role
            == UserRoleEnum.FIELD_OFFICER.value
        ):
            if self.city_payload_id or self.pincode_payload_id:
                error_field: str = "city_id" if self.city_payload_id else "pincode_id"
                return error_field, f"{error_field} {FIELD_REQUIRED_ERROR_MESSAGE}"
        # Supervisor: city required if pincodes are provided
        if user_instance.reports_to and (
            (self.reports_to_instance or user_instance.reports_to).user_role.role
            == UserRoleEnum.SUPERVISOR.value
        ):
            if self.pincode_payload_id and not self.city_payload_id:
                return "city_id", f"city_id {FIELD_REQUIRED_ERROR_MESSAGE}"
        # Validate city assignments if provided
        if self.city_payload_id:
            self.city_queryset: QuerySet[RegionConfigurationCityModel] = (
                get_user_assigned_city_queryset(
                    user_instance=self.reports_to_instance or user_instance.reports_to
                ).filter(pk__in=self.city_payload_id)
            )
            if self.city_queryset.count() != len(self.city_payload_id):
                return "city_id", INCORRECT_CITY_ID_ERROR_MESSAGE

        # Validate pincode assignments if provided
        if self.pincode_payload_id:
            self.pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
                get_user_assigned_pincode_queryset(
                    user_instance=self.reports_to_instance or user_instance.reports_to,
                    city=self.city_payload_id,
                ).filter(pk__in=self.pincode_payload_id)
            )
            if self.pincode_queryset.count() != len(self.pincode_payload_id):
                return "pincode_id", INCORRECT_PINCODE_ID_ERROR_MESSAGE

        # Validate area assignments if provided
        if self.area_payload_id:
            self.area_queryset: QuerySet[RegionConfigurationAreaModel] = (
                get_user_assigned_area_queryset(
                    user_instance=self.reports_to_instance or user_instance.reports_to,
                    pincode=self.pincode_payload_id,
                ).filter(pk__in=self.area_payload_id)
            )
            if self.area_queryset.count() != len(self.area_payload_id):
                return "area_id", INCORRECT_AREA_ID_ERROR_MESSAGE

        self.logger.info("Region-level field validation passed for user")
        return None, None

    def validate_process_level_fields(self) -> Tuple[Optional[str], Optional[str]]:
        # if not self.product_assignment_payload:
        #     return "product_assignment_id", FIELD_REQUIRED_ERROR_MESSAGE

        print("running===>")
        if self.unproduct_assignment_payload:
            subordinates = UserModel.objects.filter(reports_to=self.user_instance)
            for product_id in self.unproduct_assignment_payload:
                if UserAssignedProdudctsModel.objects.filter(
                    user__in=subordinates,
                    product_assignment_id=product_id,
                    status=CoreUtilsStatusEnum.ACTIVATED.value,
                ).exists():
                    return (
                        INVALID_PRODUCT_UNASSIGNMENT_ERROR_KEY,
                        INVALID_PRODUCT_UNASSIGNMENT_ERROR_MESSAGE,
                    )

        if not self.reports_to_instance:
            return None, None

        self.reporting_user_assigned_product_assignment_queryset: QuerySet[
            LoanConfigurationsProductAssignmentModel
        ] = get_reporting_user_assigned_product_assignment_instance(
            user_id=self.reports_to_instance.id,
            queryset=LoanConfigurationsProductAssignmentModel.objects.all(),
        )

        if (
            self.unproduct_assignment_payload
            and not self.reporting_user_assigned_product_assignment_queryset.filter(
                id__in=self.product_assignment_payload,
            ).exists()
        ):
            return (
                INVALID_PRODUCT_ASSIGNMENT_ERROR_KEY,
                INVALID_PRODUCT_ASSIGNMENT_ERROR_MESSAGE,
            )

        return None, None
        # ------

    def create(self) -> Optional[UserModel]:
        """
        Update an existing user and assign hierarchical regions/zones/cities/pincodes/areas
        in a single atomic transaction.

        Handles dependency fields and logs every assignment. Clears lower-level fields
        when higher-level fields are provided in the payload, or when role or reports_to
        changes. Only updates fields explicitly provided in the payload.

        Returns:
            Optional[UserModel]: The updated user instance, or None if update fails.
        """
        self.logger.info(f"Starting user update for user ID: {self.data.get('id')}")

        # Check if role or reports_to has changed
        role_changed: bool = (
            self.data.get("user_role")
            and str(self.user_instance.user_role.pk) != self.data["user_role"]
        )
        reports_to_changed: bool = self.data.get("reports_to") and (
            not self.user_instance.reports_to
            or str(self.user_instance.reports_to.pk) != self.data["reports_to"]
        )

        with transaction.atomic():
            # Update user fields if provided
            if self.is_status_update_method():
                self.user_instance.status = self.data["status"]
                self.user_instance.save()
                self.set_toast_message_value(value=self.user_instance.username)
                self.update_core_generic_updated_by(
                    instance=self.user_instance, log_activity=True
                )
                self.logger.info(
                    f"User status update successfully for: {self.user_instance.username}"
                )
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

            # Update UserDetail record
            user_detail_instance: UserDetailModel = UserDetailModel.objects.get(
                user=self.user_instance
            )
            if self.data.get("profile_picture"):
                user_detail_instance.profile_picture = self.data["profile_picture"]

            # Reset dependency fields if role or reports_to has changed
            if role_changed or reports_to_changed:
                self.logger.info(
                    f"{'Role' if role_changed else 'Reports_to'} changed for user {self.user_instance.username}, resetting dependency fields"
                )
                user_detail_instance.assigned_region.clear()
                user_detail_instance.assigned_zone.clear()
                user_detail_instance.assigned_city.clear()
                user_detail_instance.assigned_pincode.clear()
                user_detail_instance.assigned_area.clear()
                if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
                    self.user_instance.reports_to = (
                        None  # SR_MANAGER has no reporting manager
                    )

            # Cascading clears for hierarchy updates if higher level is received
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

            # Update region hierarchy fields based on payload if provided
            # Region (for SR_MANAGER)
            if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
                if "region_id" in self.data:
                    user_detail_instance.assigned_region.clear()  # Clear existing regions
                    if self.region_payload_id and self.region_instance:
                        user_detail_instance.assigned_region.set([self.region_instance])
                        self.logger.info(f"Assigned Region: {self.region_payload_id}")

            # Zone (for MANAGER)
            elif self.user_role_instance.role == UserRoleEnum.MANAGER.value:
                if "zone_id" in self.data:
                    user_detail_instance.assigned_zone.clear()  # Clear existing zones
                    if self.zone_payload_id and self.zone_instance:
                        user_detail_instance.assigned_zone.set([self.zone_instance])
                        self.logger.info(f"Assigned Zone: {self.zone_instance.pk}")

            # City, Pincode, Area (for SUPERVISOR or FIELD_OFFICER)
            elif self.user_role_instance.role in [
                UserRoleEnum.SUPERVISOR.value,
                UserRoleEnum.FIELD_OFFICER.value,
            ]:
                # Update cities
                if "city_id" in self.data:
                    user_detail_instance.assigned_city.clear()  # Clear existing cities
                    if self.city_queryset.exists():
                        user_detail_instance.assigned_city.set(self.city_queryset)
                        self.logger.info(
                            f"Assigned Cities: {list(self.city_queryset.values_list('pk', flat=True))}"
                        )

                # Update pincodes
                if "pincode_id" in self.data:
                    user_detail_instance.assigned_pincode.clear()  # Clear existing pincodes
                    if self.pincode_queryset.exists():
                        user_detail_instance.assigned_pincode.set(self.pincode_queryset)
                        self.logger.info(
                            f"Assigned Pincodes: {list(self.pincode_queryset.values_list('pk', flat=True))}"
                        )

                # Update areas
                if "area_id" in self.data:
                    user_detail_instance.assigned_area.clear()  # Clear existing areas
                    if self.area_queryset.exists():
                        user_detail_instance.assigned_area.set(self.area_queryset)
                        self.logger.info(
                            f"Assigned Areas: {list(self.area_queryset.values_list('pk', flat=True))}"
                        )

            # assigned_products_payload and unassigned_products_payload handling can be added here if needed

            if self.product_assignment_payload:
                valid_product_ids = (
                    LoanConfigurationsProductAssignmentModel.objects.filter(
                        pk__in=self.product_assignment_payload,
                    )
                )
                for product in valid_product_ids:
                    obj, create = UserAssignedProdudctsModel.objects.get_or_create(
                        user=self.user_instance,
                        product_assignment=product,
                        defaults={
                            "status": CoreUtilsStatusEnum.ACTIVATED.value,
                        },
                    )
                    if not create and obj.status != CoreUtilsStatusEnum.ACTIVATED.value:
                        obj.status = CoreUtilsStatusEnum.ACTIVATED.value
                        obj.save()

            if self.unproduct_assignment_payload:
                updatedcount = UserAssignedProdudctsModel.objects.filter(
                    user=self.user_instance,
                    product_assignment__in=self.unproduct_assignment_payload,
                ).update(status=CoreUtilsStatusEnum.DEACTIVATED.value)

                deactive_products = UserAssignedProdudctsModel.objects.filter(
                    user=self.user_instance,
                    product_assignment__in=self.unproduct_assignment_payload,
                )

        # !===============================================================================================================

        self.user_instance.save()
        user_detail_instance.save()

        # Set activity log details
        self.set_toast_message_value(value=self.user_instance.username)
        self.update_core_generic_updated_by(
            instance=self.user_instance, log_activity=True
        )

        self.logger.info(
            f"User update completed successfully for: {self.user_instance.username}"
        )
        return self.user_instance
