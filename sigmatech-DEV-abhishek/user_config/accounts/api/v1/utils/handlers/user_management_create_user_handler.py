from typing import List, Tuple, Callable, Optional
from django.db import transaction
from django.db.models.query import QuerySet

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.format_validator import (
    generate_valid_password,
    is_format_validator_email,
)
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
    REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE,
    REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE,
    USER_MANAGEMENT_EMAIL_ALREADY_EXISTS,
    USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT,
    USER_MANAGEMENT_LOGIN_ID_ALREADY_EXISTS,
    USER_MANAGEMENT_PHONE_NUMBER_ALREADY_EXISTS,
    USER_ROLE_INCORRECT_ERROR_MESSAGE,
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
from user_config.accounts.api.v1.utils.update_default_permissions import (
    assign_default_all_permissions,
)
from user_config.accounts.api.v1.utils.user_assigned_process_queryset import get_reporting_user_assigned_product_assignment_instance
from user_config.accounts.models import UserAssignedProdudctsModel, UserDetailModel
from user_config.user_auth.models import UserModel, UserRoleModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.utils.email_templates.user_create_email_template import (
    user_create_send_email,
)
from store.configurations.loan_config.models import LoanConfigurationsProductAssignmentModel


# Define uniqueness constraints for users
USER_UNIQUE_AND_REQUIRED_FIELD = [
    {"field": "login_id", "error_message": USER_MANAGEMENT_LOGIN_ID_ALREADY_EXISTS},
    {"field": "email", "error_message": USER_MANAGEMENT_EMAIL_ALREADY_EXISTS},
    {
        "field": "phone_number",
        "error_message": USER_MANAGEMENT_PHONE_NUMBER_ALREADY_EXISTS,
    },
]


class UserManagementCreateUserHandler(CoreGenericBaseHandler):
    """
    Handler for creating new users with strict role-based and
    region-level validations.

    Responsibilities:
    -----------------
    * Validate uniqueness and required user fields
    * Enforce role restrictions and reporting hierarchy
    * Assign appropriate region/zone/city/pincode/area mappings
    * Create both User and UserDetail records atomically
    * Log every step of validation and creation for traceability
    """

    _activity_type: str = "CONFIGURATION_USER_MANAGEMENT_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    # Role and reporting user related instances
    user_role_instance: UserRoleModel
    reports_to_instance: Optional[UserModel] = None

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
    region_payload_id: Optional[str]
    zone_payload_id: Optional[str]
    city_payload_id: List[str]
    pincode_payload_id: List[str]
    area_payload_id: List[str]
    reporting_user_assigned_product_assignment_queryset: QuerySet[
        LoanConfigurationsProductAssignmentModel]

    def set_payload(self):
        """Extract hierarchical IDs from request payload."""
        self.region_payload_id = self.data.get("region_id", None)
        self.zone_payload_id = self.data.get("zone_id", None)
        self.city_payload_id = self.data.get("city_id", [])
        self.pincode_payload_id = self.data.get("pincode_id", [])
        self.area_payload_id = self.data.get("area_id", [])
        self.product_assignment_payload_id = self.data.get(
            "product_assignment_id", [])

    def validate(self):
        """
        Run sequential validations for user creation.
        Logs each validation step and returns the first failure encountered.
        """
        self.set_payload()
        self.logger.debug(
            f"Starting validation for user creation with payload: {self.data}",
        )

        validation_methods: List[Callable] = [
            self.check_user_details_unique_and_required,
            self.validate_region_level_fields,
            self.validate_process_level_fields
        ]

        for method in validation_methods:
            field, error = method()
            if field:
                self.logger.warning(
                    f"Validation failed at {field}: {error}", )
                return self.set_error_message(error_message=error, key=field)

        self.logger.info(
            f"All validations passed successfully for user: {self.data.get("username")}",
        )

    def validate_process_level_fields(self) -> Tuple[Optional[str], Optional[str]]:
        if not self.product_assignment_payload_id:
            return "product_assignment_id", FIELD_REQUIRED_ERROR_MESSAGE
        if not self.reports_to_instance:
            return None, None
        self.reporting_user_assigned_product_assignment_queryset: QuerySet[LoanConfigurationsProductAssignmentModel] = get_reporting_user_assigned_product_assignment_instance(
            user_id=self.reports_to_instance.id,
        )
        if not self.reporting_user_assigned_product_assignment_queryset.filter(
            id__in=self.product_assignment_payload_id
        ).exists():
            return "product_assignment_id", "Product is not assigned to reporting user or invalid product"
        return None, None

    def validate_region_level_fields(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Validate region, zone, city, pincode, and area assignments
        based on the user's role and reporting manager’s permissions.
        """
        self.logger.debug(
            f"Validating region-level fields for role: {getattr(self.user_role_instance, "role", None)}",
        )

        # Region validation for SR Manager
        if self.user_role_instance.role == UserRoleEnum.SR_MANAGER.value:
            if not self.region_payload_id:
                return "region_id", FIELD_REQUIRED_ERROR_MESSAGE
            try:
                self.region_instance: RegionConfigurationRegionModel = (
                    get_user_assigned_region_queryset(
                        user_instance=self.request.user
                    ).get(pk=self.region_payload_id)
                )
                self.logger.info("Validated Region ID: %s",
                                 self.region_payload_id)
                return None, None
            except RegionConfigurationRegionModel.DoesNotExist:
                return "region_id", INCORRECT_REGION_ID_ERROR_MESSAGE

        # Zone validation for Manager
        if self.user_role_instance.role == UserRoleEnum.MANAGER.value:
            if not self.zone_payload_id:
                return "zone_id", FIELD_REQUIRED_ERROR_MESSAGE
            try:
                print("========--------=> ZONE INSTANCE: ")
                self.zone_instance: RegionConfigurationZoneModel = (
                    get_user_assigned_zone_queryset(
                        user_instance=self.reports_to_instance
                    ).get(pk=self.zone_payload_id)
                )
                print("========--------=> ZONE INSTANCEd: ", self.zone_instance)
                self.logger.info(f"Validated Zone ID: {self.zone_payload_id}")
                return None, None
            except RegionConfigurationZoneModel.DoesNotExist:
                return "zone_id", INCORRECT_ZONE_ID_ERROR_MESSAGE

        # Field Officer restriction
        if self.reports_to_instance.user_role.role == UserRoleEnum.FIELD_OFFICER.value:
            if self.city_payload_id or self.pincode_payload_id:
                error_field: str = "city_id" if self.city_payload_id else "pincode_id"
                return error_field, f"{error_field} {FIELD_REQUIRED_ERROR_MESSAGE}"

        # Supervisor: city required if pincodes are provided
        if self.reports_to_instance.user_role.role == UserRoleEnum.SUPERVISOR.value:
            if self.pincode_payload_id and not self.city_payload_id:
                return "city_id", f"city_id {FIELD_REQUIRED_ERROR_MESSAGE}"

        # Validate city assignments
        self.city_queryset: QuerySet[RegionConfigurationCityModel] = (
            get_user_assigned_city_queryset(
                user_instance=self.reports_to_instance
            ).filter(pk__in=self.city_payload_id)
        )

        if self.city_payload_id and self.city_queryset.count() != len(
            self.city_payload_id
        ):
            return "city_id", INCORRECT_CITY_ID_ERROR_MESSAGE

        # Validate pincode assignments
        self.pincode_queryset: QuerySet[RegionConfigurationPincodeModel] = (
            get_user_assigned_pincode_queryset(
                user_instance=self.reports_to_instance, city=self.city_payload_id
            ).filter(pk__in=self.pincode_payload_id)
        )

        if self.pincode_queryset.count() != len(self.pincode_payload_id):
            return "pincode_id", INCORRECT_PINCODE_ID_ERROR_MESSAGE

        # Validate area assignments
        self.area_queryset: QuerySet[RegionConfigurationAreaModel] = (
            get_user_assigned_area_queryset(
                user_instance=self.reports_to_instance, pincode=self.pincode_payload_id
            ).filter(pk__in=self.area_payload_id)
        )

        if self.area_queryset.count() != len(self.area_payload_id):
            return "area_id", INCORRECT_AREA_ID_ERROR_MESSAGE

        self.logger.info("Region-level field validation passed for user")
        return None, None

    def check_user_details_unique_and_required(
        self,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Validate user’s unique fields, role correctness, and reporting structure.
        """
        self.logger.debug(
            f"Validating unique and required user details for: {self.data.get("username")}",
        )

        # Username check
        if not self.data.get("username"):
            return "username", f"username {FIELD_REQUIRED_ERROR_MESSAGE}"

        # Check uniqueness for login_id, email, phone_number
        for field in USER_UNIQUE_AND_REQUIRED_FIELD:
            if not self.data.get(field["field"]):
                return (
                    field["field"],
                    f'{field["field"]} {FIELD_REQUIRED_ERROR_MESSAGE}',
                )
            if self.queryset.filter(
                **{field["field"]: self.data[field["field"]]}
            ).exists():
                return field["field"], field["error_message"]

        # Validate email format
        if not is_format_validator_email(email=self.data["email"]):
            return "email", USER_MANAGEMENT_EMAIL_INCORRECT_FORMAT

        # Validate role existence
        try:
            self.user_role_instance = UserRoleModel.objects.get(
                pk=self.data["user_role"]
            )
        except (KeyError, UserRoleModel.DoesNotExist):
            return "user_role", USER_ROLE_INCORRECT_ERROR_MESSAGE

        # Restrict admin role creation
        if self.user_role_instance.role == UserRoleEnum.ADMIN.value:
            return "user_role", ADMIN_ROLE_NOT_ALLOWED_ERROR_MESSAGE

        # Check role creation permissions
        if not has_user_permission_to_role(self.request.user, self.user_role_instance):
            return (
                "user_role",
                REPORTING_USER_HAS_NO_PERMISSION_TO_USER_ROLE_ERROR_MESSAGE,
            )

        # Validate reporting user
        if self.user_role_instance.role != UserRoleEnum.SR_MANAGER.value:
            if not self.data.get("reports_to"):
                return "reports_to", f"reports_to {FIELD_REQUIRED_ERROR_MESSAGE}"

            if not self.queryset.filter(pk=self.data["reports_to"]).exists():
                return "reports_to", INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE

            try:
                self.reports_to_instance: UserModel = self.queryset.get(
                    pk=self.data["reports_to"]
                )
            except UserModel.DoesNotExist:
                return "reports_to", INCORRECT_REPORTS_TO_ID_ERROR_MESSAGE

            sub_ordinate_user_ids: List[str] = list_of_user_id_under_user_instance(
                self.request.user
            )

            if str(self.reports_to_instance.pk) not in sub_ordinate_user_ids:
                return "reports_to", REPORTS_TO_USER_IS_NOT_LOGIN_USER_SUB_ORDINATE

        self.logger.info("Unique and required user detail validation passed")
        return None, None

    def create(self):
        """
        Create a new user and assign hierarchical regions/zones/cities/pincodes/areas
        in a single atomic transaction. Logs every assignment.
        """
        self.logger.info(
            f"Starting user creation for username:  {self.data.get("username")}",
        )

        with transaction.atomic():
            # Create base user
            user_instance: UserModel = self.queryset.create(
                username=self.data["username"],
                login_id=self.data["login_id"],
                email=self.data["email"],
                phone_number=self.data["phone_number"],
                user_role=self.user_role_instance,
                reports_to=self.reports_to_instance,
                **{"is_active": True, "is_verified": True, "is_approved": True},
            )
            self.logger.debug(f"Created User instance: {user_instance}")

            # Generate and assign password
            password = generate_valid_password()
            user_instance.set_password(password)
            user_instance.save()
            self.logger.info(
                f"Password set for User: {user_instance.username} with {password}"
            )

            # Create UserDetail record
            user_detail_instance: UserDetailModel = UserDetailModel.objects.create(
                user=user_instance,
                profile_picture=self.data.get("profile_picture", None),
            )
            self.logger.debug(
                f"Created UserDetail instance for user: {user_instance.username}"
            )

            # Assign regions/zones/cities/pincodes/areas if validated
            if self.region_instance:
                user_detail_instance.assigned_region.add(
                    self.region_payload_id)
                self.logger.info(f"Assigned Region: {self.region_payload_id}")

            if self.zone_instance:
                user_detail_instance.assigned_zone.add(self.zone_instance)
                self.logger.info(f"Assigned Zone: {self.zone_instance.pk}")

            if self.city_queryset.exists():
                user_detail_instance.assigned_city.set(self.city_queryset)
                self.logger.info(
                    f"Assigned Cities: {list(self.city_queryset.values_list('pk', flat=True))}"
                )

            if self.pincode_queryset.exists():
                user_detail_instance.assigned_pincode.set(
                    self.pincode_queryset)
                self.logger.info(
                    f"Assigned Pincodes: {list(self.pincode_queryset.values_list("pk", flat=True))}"
                )

            if self.area_queryset.exists():
                user_detail_instance.assigned_area.set(self.area_queryset)
                self.logger.info(
                    f"Assigned Areas: {list(
                        self.area_queryset.values_list("pk", flat=True))}"
                )

                # !==================================================================

            if self.product_assignment_payload_id:
                valid_product_qs = LoanConfigurationsProductAssignmentModel.objects.filter(
                    pk__in=self.product_assignment_payload_id
                )
            
            print("================> VALID PRODUCT QS: ", valid_product_qs)

             # Bulk create for efficiency
            UserAssignedProdudctsModel.objects.bulk_create(
                [
                    UserAssignedProdudctsModel(
                        user=user_instance, product_assignment=product
                    )
                    for product in valid_product_qs
                ],
                ignore_conflicts=True,  # avoids duplicate entries due to unique_together
            )
            # != == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

            user_detail_instance.save()

            assign_default_all_permissions(user_instance=user_instance)
            self.logger.info("Permissions assigned successfully")
            # Set activity log details
            self.set_toast_message_value(value=user_instance.username)
            self.update_core_generic_created_by(instance=user_instance)
            user_create_send_email(
                user_instance=user_instance, password=password)

        self.logger.info(
            f"User creation completed successfully for: {user_instance.username}"
        )
