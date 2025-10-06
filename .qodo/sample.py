from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid


class LoanConfigurationsProcessModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BANK_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="BANK_NAME",
    )
    logo = models.URLField(
        null=True,
        blank=True,
        db_column="BANK_LOGO",
    )

    contact_person_name = models.CharField(
        max_length=100, null=True, blank=True, db_column="CONTACT_PERSON_NAME"
    )
    contact_person_email = models.CharField(
        max_length=100, null=True, blank=True, db_column="CONTACT_PERSON_EMAIL"
    )
    contact_person_phone_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column="CONTACT_PERSON_PHONE_NUMBER",
    )

    class Meta:
        db_table = "BANK_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_process_title"),
        ]
        verbose_name = "Process"
        verbose_name_plural = "Processs"


class LoanConfigurationsProductsModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="PRODUCT_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="PRODUCT_NAME",
    )

    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="PRODUCT_DESCRIPTION"
    )

    class Meta:
        db_table = "PRODUCT_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_product_title"),
        ]


class LoanConfigurationsMonthlyCycleModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="CYCLE_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="CYCLE_NAME",
    )

    # added description field
    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="CYCLE_DESCRIPTION"
    )

    class Meta:
        db_table = "MONTHLY_CYCLE_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_cycle_title"),
        ]


class BucketRangeModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_column="BUCKET_RANGE_ID",
    )
    label = models.CharField(
        max_length=50,
        db_column="BUCKET_RANGE_LABEL",
    )
    # value = models.PositiveIntegerField(db_column="BUCKET_RANGE_VALUE")

    # value as string not int
    value = models.CharField(
        max_length=50,
        db_column="BUCKET_RANGE_VALUE",
    )

    class Meta:
        db_table = "BUCKET_RANGE_TABLE"
        indexes = [
            models.Index(fields=["label"], name="idx_bucket_range_label"),
        ]


class LoanConfigurationsBucketModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BUCKET_ID",
        default=uuid.uuid4,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        db_column="BUCKET_NAME",
    )
    description = models.CharField(
        max_length=200, null=True, blank=True, db_column="BUCKET_DESCRIPTION"
    )

    range = models.ForeignKey(
        BucketRangeModel,
        on_delete=models.CASCADE,
        null=True,
        db_column="BUCKET_RANGE_ID",
        related_name="LoanConfigurationsBucketModel_range",
    )

    class Meta:
        db_table = "BUCKET_TABLE"
        indexes = [
            models.Index(fields=["title"], name="idx_bucket_title"),
        ]


class LoanConfigurationsProductAssignmentModel(CoreGenericModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        db_column="BANK_PRODUCT_ASSIGNMENT_ID",
        default=uuid.uuid4,
    )
    process = models.ForeignKey(
        LoanConfigurationsProcessModel,
        on_delete=models.CASCADE,
        related_name="LoanConfigurationsProductAssignmentModel_process",
        db_column="BANK_ID",
    )
    product = models.ForeignKey(
        LoanConfigurationsProductsModel,
        on_delete=models.CASCADE,
        related_name="LoanConfigurationsProductAssignmentModel_product",
        db_column="PRODUCT_ID",
    )
    min_due_percentage = models.FloatField(
        null=True,
        blank=True,
        db_column="MIN_DUE_PERCENTAGE",
    )
    refer_back_percentage = models.FloatField(
        null=True,
        blank=True,
        db_column="REFER_BACK_PERCENTAGE",
    )

    class Meta:
        db_table = "BANK_PRODUCT_ASSIGNMENT_TABLE"
        indexes = [
            models.Index(fields=["process"]),
            models.Index(fields=["product"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["process", "product"], name="UNIQUE_BANK_PRODUCT"
            ),
        ]  from django.db import models
        from core_utils.region_data.models import PincodeModel
        from core_utils.utils.generics.generic_models import CoreGenericModel
        import uuid
        
        from store.configurations.region_config.queryset import (
            AreaQuerySet,
            CityQuerySet,
            PincodeQuerySet,
            RegionQuerySet,
            ZoneQuerySet,
        )
        
        
        class RegionConfigurationRegionModel(CoreGenericModel):
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid1, editable=False, db_column="REGION_ID"
            )
            title = models.CharField(max_length=50, unique=True, db_column="REGION")
            description = models.CharField(
                max_length=100, null=True, blank=True, db_column="DESCRIPTION"
            )
            objects = RegionQuerySet.as_manager()
        
            class Meta:
                db_table = "REGION_TABLE"
                indexes = [
                    models.Index(fields=["title"]),
                ]
        
            def __str__(self):
                return self.title
        
        
        class RegionConfigurationZoneModel(CoreGenericModel):
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid1, editable=False, db_column="ZONE_ID"
            )
            title = models.CharField(max_length=100, unique=True, db_column="ZONE")
            region = models.ForeignKey(
                RegionConfigurationRegionModel,
                on_delete=models.CASCADE,
                related_name="RegionConfigurationZoneModel_region",
                db_column="REGION_ID",
            )
            description = models.CharField(
                max_length=100, null=True, blank=True, db_column="DESCRIPTION"
            )
            objects = ZoneQuerySet.as_manager()
        
            class Meta:
                db_table = "ZONE_TABLE"
                indexes = [
                    models.Index(fields=["region"]),
                    models.Index(fields=["title"]),
                ]
        
            def __str__(self):
                return self.title
        
        
        class RegionConfigurationCityModel(CoreGenericModel):
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid1, editable=False, db_column="CITY_ID"
            )
            city_name = models.CharField(
                max_length=50,
                null=True,
                db_column="CITY_NAME",
            )
            zone = models.ForeignKey(
                RegionConfigurationZoneModel,
                related_name="RegionConfigurationCityModel_zone",
                on_delete=models.CASCADE,
                db_column="ZONE_ID",
            )
            description = models.CharField(
                max_length=100, null=True, blank=True, db_column="DESCRIPTION"
            )
            objects = CityQuerySet.as_manager()
        
            class Meta:
                db_table = "CITY_TABLE"
                indexes = [
                    models.Index(fields=["zone"]),
                    models.Index(fields=["city_name"]),
                ]
        
            def __str__(self):
                return self.city_name
        
        
        class RegionConfigurationPincodeModel(CoreGenericModel):
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid1, editable=False, db_column="PINCODE_ID"
            )
            pincode = models.OneToOneField(
                PincodeModel,
                on_delete=models.CASCADE,
                related_name="RegionConfigurationPincodeModel_pincode",
                db_column="PINCODE",
            )
            city = models.ForeignKey(
                RegionConfigurationCityModel,
                on_delete=models.CASCADE,
                db_column="CITY_ID",
                related_name="RegionConfigurationPincodeModel_city",
            )
        
            objects = PincodeQuerySet.as_manager()
        
            class Meta:
                db_table = "PINCODE_TABLE"
                indexes = [
                    models.Index(fields=["city"]),
                    models.Index(fields=["pincode"]),
                ]
        
            def __str__(self):
                return self.pincode.pincode
        
        
        class RegionConfigurationAreaModel(CoreGenericModel):
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid1, editable=False, db_column="AREA_ID"
            )
            title = models.CharField(max_length=255, unique=True, db_column="AREA_NAME")
            pincode = models.ForeignKey(
                RegionConfigurationPincodeModel,
                on_delete=models.CASCADE,
                db_column="PINCODE_ID",
                related_name="RegionConfigurationAreaModel_pincode",
            )
        
            objects = AreaQuerySet.as_manager()
        
            class Meta:
                db_table = "AREA_TABLE"
                unique_together = ("title", "pincode")
                indexes = [
                    models.Index(fields=["pincode"]),
                    models.Index(fields=["title"]),
                ]
        
            def __str__(self):
                return self.title
         import uuid
         from django.db import models
         
         from core_utils.utils.generics.generic_models import CoreGenericModel
         from store.configurations.loan_config.models import LoanConfigurationsProductAssignmentModel
         from store.configurations.region_config.models import (
             RegionConfigurationAreaModel,
             RegionConfigurationCityModel,
             RegionConfigurationPincodeModel,
             RegionConfigurationRegionModel,
             RegionConfigurationZoneModel,
         )
         from user_config.user_auth.enums import BloodGroupEnum, EmergencyContactRelationEnum
         from user_config.user_auth.models import UserModel
         
         # Create your models here.
         
         
         class UserDetailModel(CoreGenericModel):
             user = models.OneToOneField(
                 UserModel,
                 primary_key=True,
                 unique=True,
                 related_name="UserDetailModel_user",
                 on_delete=models.CASCADE,
                 db_column="USER_AUTH_ID",
                 # editable=False,
             )
         
             profile_picture = models.URLField(
                 max_length=1000, null=True, blank=True, db_column="PROFILE_PICTURE"
             )
         
             blood_group = models.CharField(
                 max_length=20,
                 choices=BloodGroupEnum.choices(),
                 db_column="BLOOD_GROUP",
                 null=True,
                 blank=True,
             )
         
             vehicle_number = models.CharField(
                 max_length=100, db_column="VEHICLE", null=True, blank=True
             )
             emergency_phone_number = models.CharField(
                 max_length=10,
                 null=True,
                 blank=True,
                 db_column="EMERGENCY_PHONE_NUMBER",
             )
             emergency_contact_relation_name = models.CharField(
                 max_length=10,
                 null=True,
                 blank=True,
                 choices=EmergencyContactRelationEnum.choices(),
                 db_column="EMERGENCY_CONTACT_RELATION_NAME",
             )
             emergency_contact_relation = models.CharField(
                 max_length=10,
                 null=True,
                 blank=True,
                 choices=EmergencyContactRelationEnum.choices(),
                 db_column="EMERGENCY_CONTACT_RELATION",
             )
         
             # sr manager are assigned to entire Region
             assigned_region = models.ManyToManyField(
                 RegionConfigurationRegionModel,
                 blank=True,
                 related_name="UserDetailModel_assigned_region",
                 db_column="ASSIGNED_REGION_ID",
             )
             # manager are assigned to entire zone
             assigned_zone = models.ManyToManyField(
                 RegionConfigurationZoneModel,
                 blank=True,
                 related_name="UserDetailModel_assigned_zone",
                 db_column="ASSIGNED_ZONE_ID",
             )
             # supervisor are assigned to entire one or more than one city
             assigned_city = models.ManyToManyField(
                 RegionConfigurationCityModel,
                 blank=True,
                 related_name="UserDetailModel_assigned_city",
                 db_column="ASSIGNED_ZONE_ID",
             )
             # field agent's are assigned to one or more than one pincode or area
         
             assigned_pincode = models.ManyToManyField(
                 RegionConfigurationPincodeModel,
                 blank=True,
                 related_name="UserDetailModel_assigned_pincode",
                 db_column="ASSIGNED_PINCODE_ID",
             )
         
             assigned_area = models.ManyToManyField(
                 RegionConfigurationAreaModel,
                 blank=True,
                 related_name="UserDetailModel_assigned_area",
                 db_column="ASSIGNED_AREA_ID",
             )
         
             class Meta:
                 db_table = "USER_DETAIL_TABLE"
         
             def __str__(self):
                 if self.user and hasattr(self.user, 'username'):
                     return str(self.user.username or "")
                 return "User Detail"
          
         
         class UserAssignedProdudctsModel(CoreGenericModel):
             id = models.UUIDField(
                 primary_key=True,
                 unique=True,
                 editable=False,
                 db_column="USER_ASSIGNED_PRODUCTS__ID",
                 default=uuid.uuid4,
             )
             user = models.ForeignKey(
                 UserModel,
                 on_delete=models.CASCADE,
                 related_name="UserAssignedProdudctsModel_user",
                 db_column="USER_AUTH_ID",
                 # editable=False,
             )
             product_assignment = models.ForeignKey(
                 LoanConfigurationsProductAssignmentModel,
                 on_delete=models.CASCADE,
                 related_name="UserAssignedProdudctsModel_product_assignment",
                 db_column="PRODUCT_ASSIGNMENT_ID",
             )
         
             class Meta:
                 db_table = "USER_ASSIGNED_PRODUCTS_TABLE"
                 unique_together = ("user", "product_assignment")
         import uuid
         from django.db import models
         from core_utils.utils.generics.generic_models import CoreGenericModel
         from user_config.user_auth.models import UserModel
         
         # Create your models here.
         
         
         class UserConfigPermissionsActionsModel(CoreGenericModel):
             id = models.UUIDField(
                 primary_key=True,
                 default=uuid.uuid1,
                 editable=False,
                 db_column="PERMISSION_ACTION_ID",
             )
             title = models.CharField(max_length=100, db_column="ACTION_TYPE")
         
             class Meta:
                 db_table = "PERMISSION_ACTION_TABLE"
         
             def __str__(self):
                 return self.title
         
         
         class UserConfigPermissionsModel(CoreGenericModel):
             id = models.UUIDField(
                 primary_key=True, default=uuid.uuid1, editable=False, db_column="PERMISSION_ID"
             )
             title = models.CharField(max_length=100, db_column="PERMISSION")
             description = models.CharField(
                 max_length=512, db_column="DESCRIPTION", null=True, blank=True
             )
             icons = models.URLField(
                 max_length=512, db_column="ICONS_URL", null=True, blank=True
             )
         
             parent_permission = models.ForeignKey(
                 "self",
                 on_delete=models.CASCADE,
                 related_name="UserConfigPermissionsModel_parent_permission",
                 db_column="PARENT_PERMISSION_ID",
                 null=True,
                 blank=True,
             )
         
             def __str__(self):
                 return self.title
         
             class Meta:
                 db_table = "PERMISSION_TABLE"
         
         
         class UserConfigUserAssignedPermissionsModel(CoreGenericModel):
             id = models.UUIDField(
                 primary_key=True,
                 default=uuid.uuid1,
                 editable=False,
                 db_column="USER_ASSIGNED_PERMISSION_ID",
             )
             permission = models.ForeignKey(
                 UserConfigPermissionsModel,
                 on_delete=models.CASCADE,
                 related_name="UserConfigUserAssignedPermissionsModel_permission",
                 db_column="PERMISSION_ID",
             )
             user = models.ForeignKey(
                 UserModel,
                 on_delete=models.CASCADE,
                 related_name="UserConfigUserAssignedPermissionsModel_user",
                 db_column="USER_ID",
             )
             read_only_access = models.BooleanField(default=False, db_column="READ_ONLY_ACCESS")
             all_access = models.BooleanField(default=False, db_column="ALL_ACCESS")
         
             class Meta:
                 db_table = "USER_ASSIGNED_PERMISSION_TABLE"
                 unique_together = ("permission", "user")                                     import uuid
                 
                 from django.apps import apps
                 from django.contrib.auth.models import (
                     AbstractBaseUser,
                     BaseUserManager,
                     PermissionsMixin,
                 )
                 from django.db import models, transaction
                 
                 from core_utils.utils.generics.generic_models import CoreGenericModel
                 from user_config.user_auth.enums import UserRoleEnum
                 
                 
                 # Create your models here.
                 
                 
                 class UserRoleModel(CoreGenericModel):
                     id = models.UUIDField(
                         primary_key=True, default=uuid.uuid1, editable=False, db_column="USER_ROLE_ID"
                     )
                     title = models.CharField(max_length=100, db_column="USER_ROLE")
                     role = models.CharField(
                         max_length=20, choices=UserRoleEnum.choices(), db_column="ROLE", unique=True
                     )
                     icons = models.CharField(max_length=512, null=True, blank=True, db_column="ICONS")
                     reports_to = models.ForeignKey(
                         "self",
                         on_delete=models.CASCADE,
                         related_name="UserRoleModel_reports_to",
                         db_column="REPORTS_TO_ID",
                         null=True,
                         blank=True,
                     )
                 
                     def __str__(self):
                         return self.title
                 
                     # class Meta:
                     #     db_table = "USER_ROLE_TABLE"
                 
                 
                 class CustomUserManager(BaseUserManager):
                     """
                     Object Manager for UserModel
                     """
                 
                     def create_user(
                         self, login_id: str, password: str = None, **extra_fields
                     ) -> AbstractBaseUser:
                         """
                         This is a manager method to create a user
                         """
                         with transaction.atomic():
                             if not login_id:
                                 raise ValueError("login_id is required")
                 
                             user: AbstractBaseUser = self.model(login_id=login_id, **extra_fields)
                 
                             if password:
                                 user.set_password(password)
                 
                             user.save(using=self._db)
                             user_detail_model: models.Model = apps.get_model("accounts.UserDetailModel")
                             # ? Automatically create a UserDetailModel entry
                             user_detail_model.objects.create(user=user)
                 
                         return user
                 
                     def create_superuser(self, login_id: str, password: str) -> AbstractBaseUser:
                         """
                         This is a manager method to create a superuser
                         """
                         extra_fields: dict = {
                             "email": f"{login_id}@mail.com",
                             "is_superuser": True,
                             "is_active": True,
                             "is_approved": True,
                             "is_verified": True,
                             "is_staff": True,
                         }
                 
                         return self.create_user(login_id=login_id, password=password, **extra_fields)
                 
                 
                 class UserModel(AbstractBaseUser, PermissionsMixin, CoreGenericModel):
                     id = models.UUIDField(
                         unique=True,
                         primary_key=True,
                         default=uuid.uuid1,
                         db_column="USER_AUTH_ID",
                         editable=False,
                     )
                     username = models.CharField(
                         max_length=256, null=True, blank=True, db_column="USERNAME"
                     )
                     email = models.EmailField(max_length=100, db_column="EMAIL", unique=True)
                     login_id = models.CharField(max_length=100, db_column="LOGIN_ID", unique=True)
                     user_role = models.ForeignKey(
                         UserRoleModel,
                         on_delete=models.CASCADE,
                         related_name="UserModel_user_role",
                         db_column="USER_ROLE_JOB_ID",
                         null=True,
                         blank=True,
                     )
                     reports_to = models.ForeignKey(
                         "self",
                         on_delete=models.CASCADE,
                         related_name="UserModel_reports_to",
                         db_column="REPORTS_TO",
                         null=True,
                         blank=True,
                     )
                     phone_number = models.CharField(
                         max_length=100, db_column="PHONE_NUMBER", blank=True, unique=True
                     )
                     # ? Permissions
                     # ? Default django abstract Permissions
                     is_staff = models.BooleanField(default=False, db_column="IS_STAFF")
                     is_active = models.BooleanField(default=False, db_column="IS_ACTIVE")
                     is_verified = models.BooleanField(default=False, db_column="IS_VERIFIED")
                     is_superuser = models.BooleanField(default=False, db_column="IS_SUPERUSER")
                     # ? custom permissions
                     is_approved = models.BooleanField(default=False, db_column="IS_APPROVED")
                 
                     last_login = models.DateTimeField(null=True, blank=True, db_column="LAST_LOGIN")
                 
                     created_date = models.DateTimeField(auto_now_add=True, db_column="CREATED_DATE")
                     updated_date = models.DateTimeField(auto_now=True, db_column="UPDATED_DATE")
                 
                     USERNAME_FIELD = "login_id"
                 
                     objects = CustomUserManager()
                 
                     def has_perm(self, perm, obj=None):
                         return True
                 
                     def has_module_perms(self, app_label):
                         return True
                 
                     class Meta:
                         db_table = "USER_AUTH_TABLE"
                 
                 
                 class BlackListTokenModel(CoreGenericModel):
                     id = models.UUIDField(
                         db_column="BLACKLIST_TOKEN_ID",
                         default=uuid.uuid1,
                         unique=True,
                         primary_key=True,
                         editable=False,
                     )
                     token = models.TextField(db_column="JWT_TOKEN")
                     user = models.ForeignKey(
                         UserModel,
                         on_delete=models.CASCADE,
                         related_name="BlackListTokenModel_user",
                         db_column="USER_ID",
                     )
                     is_login = models.BooleanField(default=False, db_column="IS_LOGIN")
                     is_delete = models.BooleanField(default=False, db_column="IS_DELETE")
                 
                     class Meta:
                         db_table = "USER_BLACK_LIST_TOKEN_TABLE"
                 
                 
                 class LoginAnalyticsModel(CoreGenericModel):
                     id = models.UUIDField(
                         db_column="USER_LOGIN_ANALYTICS_ID",
                         default=uuid.uuid1,
                         unique=True,
                         primary_key=True,
                         editable=False,
                     )
                     ip_address = models.CharField(
                         max_length=255, db_column="IP_ADDRESS", null=True, blank=True
                     )
                     user = models.ForeignKey(
                         UserModel,
                         on_delete=models.CASCADE,
                         related_name="LoginAnalyticsModel_user",
                         db_column="USER_ID",
                     )
                     login_count = models.IntegerField(default=0, db_column="LOGIN_COUNT")
                     device_name = models.CharField(max_length=255, db_column="DEVICE_NAME")
                     token = models.TextField(null=True, blank=True, db_column="TOKEN")
                 
                     class Meta:
                         db_table = "USER_LOGIN_ANALYTICS_TABLE"  import datetime
                         from django.db import models
                         import uuid
                         from core_utils.utils.generics.generic_models import CoreGenericModel
                         from store.configurations.loan_config.models import (
                             LoanConfigurationsMonthlyCycleModel,
                             LoanConfigurationsProductAssignmentModel,
                         )
                         
                         
                         class AllocationFileModel(CoreGenericModel):
                             id = models.UUIDField(
                                 unique=True,
                                 primary_key=True,
                                 default=uuid.uuid1,
                                 db_column="ALLOCATION_FILE_ID",
                                 editable=False,
                             )
                             title = models.CharField(
                                 max_length=255,
                                 unique=True,
                                 db_column="ALLOCATION_FILE_NAME",
                             )
                             file_url = models.URLField(
                                 max_length=512,
                                 null=True,
                                 blank=True,
                                 db_column="FILE_URL",
                             )
                             latest_reupload_file_url = models.URLField(
                                 max_length=512,
                                 null=True,
                                 blank=True,
                                 db_column="LATEST_REUPLOAD_FILE_URL",
                             )
                             latest_error_file_url = models.URLField(
                                 max_length=512,
                                 null=True,
                                 blank=True,
                                 db_column="LATEST_ERROR_FILE_URL",
                             )
                             cycle = models.ForeignKey(
                                 LoanConfigurationsMonthlyCycleModel,
                                 on_delete=models.CASCADE,
                                 related_name="AllocationFileModel_cycle",
                                 db_column="CYCLE_ID",
                             )
                             product_assignment = models.ForeignKey(
                                 LoanConfigurationsProductAssignmentModel,
                                 on_delete=models.CASCADE,
                                 related_name="AllocationFileModel_product_assignment",
                                 db_column="PROCESS_PRODUCT_ASSIGNMENT_ID",
                             )
                             no_of_total_records = models.IntegerField(
                                 default=0,
                                 db_column="NO_OF_TOTAL_RECORDS",
                             )
                             no_of_valid_records = models.IntegerField(
                                 default=0,
                                 db_column="NO_OF_VALID_RECORDS",
                             )
                             no_of_error_records = models.IntegerField(
                                 default=0,
                                 db_column="NO_OF_ERROR_RECORDS",
                             )
                             no_of_duplicate_records = models.IntegerField(
                                 default=0,
                                 db_column="NO_OF_DUPLICATE_RECORDS",
                             )
                             expiry_date = models.DateTimeField(
                                 null=True,
                                 blank=True,
                                 db_column="ALLOCATION_FILE_EXPIRY_DATE",
                             )
                         
                             def save(self, *args, **kwargs) -> None:
                                 """
                                 Override the save method to compute the expiry_date based on core_generic_created_at
                                 and cycle.title.
                         
                                 Assumes cycle.title is a string or integer representing the number of days.
                                 If cycle.title is not a valid integer, raises a ValueError.
                                 """
                                 if not self.expiry_date:
                                     try:
                                         # Convert cycle.title to an integer
                                         cycle_days = int(self.cycle.title)
                                         # Calculate expiry_date based on core_generic_created_at and cycle.title
                                         self.expiry_date = self.core_generic_created_at + datetime.timedelta(
                                             days=cycle_days
                                         )
                                     except (ValueError, TypeError):
                                         raise ValueError(
                                             "cycle.title must be a valid integer representing days"
                                         )
                         
                                 super().save(*args, **kwargs)
                         
                             class Meta:
                                 db_table = "ALLOCATION_FILE_TABLE"
                                 # indexes = [
                                 #     models.Index(fields=["cycle"], name="idx_alloc_cycle"),
                                 #     models.Index(
                                 #         fields=["product_assignment"], name="idx_alloc_product_assignment"
                                 #     ),
                                 #     models.Index(fields=["expiry_date"], name="idx_alloc_expiry_date"),
                                 # ]
                         import uuid
                         from django.db import models
                         from core_utils.utils.generics.generic_models import CoreGenericModel
                         from store.configurations.loan_config.template_config.enums import SQLDataTypeEnum
                         from store.operations.allocation_files.models import AllocationFileModel
                         from store.operations.referal_files.models import ReferalFileModel
                         from store.operations.case_management.enums import (
                             CaseLifecycleStageEnum,
                             RiskTypesEnum,
                         )
                         from store.configurations.loan_config.models import LoanConfigurationsBucketModel
                         from store.configurations.region_config.models import (
                             RegionConfigurationCityModel,
                             RegionConfigurationPincodeModel,
                         )
                         
                         
                         class CaseLifecycleStageModel(CoreGenericModel):
                             """
                             Model to store lifecycle stages for case management.
                             """
                         
                             id = models.UUIDField(
                                 unique=True,
                                 primary_key=True,
                                 default=uuid.uuid1,
                                 db_column="CASE_LIFE_CYCLE_STAGE_ID",
                                 editable=False,
                             )
                             title = models.CharField(
                                 max_length=255,
                                 choices=CaseLifecycleStageEnum.choices(),
                                 db_column="CASE_LIFE_CYCLE_STAGE",
                             )
                         
                             class Meta:
                                 db_table = "CASE_LIFE_CYCLE_STAGE_TABLE"
                                 indexes = [
                                     models.Index(fields=["title"], name="idx_stage_title"),
                                 ]
                         
                             def __str__(self) -> str:
                                 return str(self.title or "")
                         
                         
                         class CaseLifecycleDispositionModel(CoreGenericModel):
                             """
                             Model to store disposition types for case management.
                             """
                         
                             id = models.UUIDField(
                                 unique=True,
                                 primary_key=True,
                                 default=uuid.uuid1,
                                 db_column="CASE_LIFE_CYCLE_DISPOSITION_ID",
                                 editable=False,
                             )
                             title = models.CharField(
                                 max_length=255,
                                 db_column="DISPOSITION",
                                 unique=True,
                             )
                             enum = models.CharField(
                                 max_length=255,
                                 choices=CaseLifecycleStageEnum.choices(),
                                 db_column="DISPOSITION_ENUM",
                             )
                             short_forms = models.CharField(
                                 max_length=50,
                                 db_column="DISPOSITION_SHORT_FORM",
                             )
                         
                             class Meta:
                                 db_table = "CASE_LIFE_DISPOSITION_TABLE"
                                 # indexes = [
                                 #     models.Index(fields=["title"], name="idx_disposition_title"),
                                 #     models.Index(fields=["enum"], name="idx_disposition_enum"),
                                 #     models.Index(fields=["short_forms"], name="idx_disposition_short_forms"),
                                 # ]
                         
                             def __str__(self) -> str:
                                 return str(self.title or "")
                         
                         
                         class AddressTypeModel(CoreGenericModel):
                             """
                             Master table for address types (Home, Office, Billing, Shipping, etc.)
                             """
                         
                             id = models.UUIDField(
                                 unique=True,
                                 primary_key=True,
                                 default=uuid.uuid1,
                                 db_column="ADDRESS_TYPE_ID",
                                 editable=False,
                             )
                             title = models.CharField(
                                 max_length=50,
                                 unique=True,
                                 db_column="ADDRESS_TYPE_TITLE",
                             )
                         
                             class Meta:
                                 db_table = "ADDRESS_TYPE_TABLE"
                                 indexes = [
                                     models.Index(fields=["title"], name="idx_address_type_title"),
                                 ]
                         
                             def __str__(self) -> str:
                                 return str(self.title or "")
                         
                         
                         class CaseManagementCaseModel(CoreGenericModel):
                             """
                             Model to store case management details, including customer information, loan details,
                             and lifecycle status. Supports all possible fields for various loan types, with
                             mandatory fields validated for template processing.
                             """
                         
                             id = models.UUIDField(
                                 unique=True,
                                 primary_key=True,
                                 default=uuid.uuid1,
                                 db_column="CASE_MANAGEMENT_ID",
                                 editable=False,
                             )
                             allocation_file = models.ForeignKey(
                                 AllocationFileModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_allocation_file",
                                 db_column="ALLOCATION_FILE_ID",
                             )
                             referal_file = models.ForeignKey(
                                 ReferalFileModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_referal_file",
                                 db_column="REFERAL_FILE_ID",
                                 null=True,
                                 blank=True,
                             )
                             status = models.ForeignKey(
                                 CaseLifecycleStageModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_status",
                                 null=True,
                                 blank=True,
                                 db_column="STATUS_ID",
                             )
                             disposition = models.ForeignKey(
                                 CaseLifecycleDispositionModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_disposition",
                                 null=True,
                                 blank=True,
                                 db_column="DISPOSITION_ID",
                             )
                             risk = models.CharField(
                                 max_length=32,
                                 choices=RiskTypesEnum.choices(),
                                 null=True,
                                 blank=True,
                                 db_column="RISK_TYPE",
                             )
                             bucket = models.ForeignKey(
                                 LoanConfigurationsBucketModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_bucket",
                                 blank=False,
                                 null=False,
                                 db_column="BUCKET_ID",
                             )
                             # Customer Personal Details
                             customer_name = models.CharField(
                                 max_length=255,
                                 blank=False,
                                 null=False,
                                 db_column="CUSTOMER_NAME",
                             )
                             father_name = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="FATHER_NAME",
                             )
                             customer_dob = models.DateField(
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMER_DOB",
                             )
                             customer_personal_email_id = models.EmailField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMER_PERSONAL_EMAIL_ID",
                             )
                             customer_pan_number = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMER_PAN_NUMBER",
                             )
                             primary_number = models.CharField(
                                 max_length=20,
                                 blank=False,
                                 null=False,
                                 db_column="PRIMARY_NUMBER",
                             )
                             alternate_number_1 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="ALTERNATE_NUMBER_1",
                             )
                             alternate_number_2 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="ALTERNATE_NUMBER_2",
                             )
                             alternate_number_3 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="ALTERNATE_NUMBER_3",
                             )
                             alternate_number_4 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="ALTERNATE_NUMBER_4",
                             )
                         
                             # Customer Demographic Details (Office/Employer Address)
                             customer_employer_office_name = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMER_EMPLOYER_OFFICE_NAME",
                             )
                         
                             customers_office_email_id = models.EmailField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMERS_OFFICE_EMAIL_ID",
                             )
                             occupation_type = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="OCCUPATION_TYPE",
                             )
                             customer_bank = models.CharField(
                                 max_length=100,
                                 blank=True,
                                 null=True,
                                 db_column="CUSTOMER_BANK",
                             )
                             # Loan Account & Product Details
                             loan_account_number = models.CharField(
                                 max_length=50,
                                 blank=False,
                                 null=False,
                                 db_column="LOAN_ACCOUNT_NUMBER",
                             )
                             card_number = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="CARD_NUMBER",
                             )
                             crn_number = models.CharField(
                                 max_length=50,
                                 unique=True,
                                 blank=False,
                                 null=False,
                                 db_column="CRN_NUMBER",
                             )
                             pool_type = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="POOL_TYPE",
                             )
                             vehicle_number = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="VEHICLE_NUMBER",
                             )
                             asset_make = models.CharField(
                                 max_length=100,
                                 blank=True,
                                 null=True,
                                 db_column="ASSET_MAKE",
                             )
                             tenure = models.IntegerField(
                                 blank=True,
                                 null=True,
                                 db_column="TENURE",
                             )
                             engineno = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="ENGINENO",
                             )
                             chassisno = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="CHASSISNO",
                             )
                             # Financial Summary
                             credit_limit = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="CREDIT_LIMIT",
                             )
                             cash_limit = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="CASH_LIMIT",
                             )
                             total_loan_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="TOTAL_LOAN_AMOUNT",
                             )
                             pos_value = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="POS_VALUE",
                             )
                             emi_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="EMI_AMOUNT",
                             )
                             minimum_due_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="MINIMUM_DUE_AMOUNT",
                             )
                             collectable_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 db_column="COLLECTABLE_AMOUNT",
                             )
                             penalty_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 db_column="PENALTY_AMOUNT",
                             )
                             late_payment_fee = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 db_column="LATE_PAYMENT_FEE",
                             )
                             late_payment_charges = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 db_column="LATE_PAYMENT_CHARGES",
                             )
                             number_of_emi_paid = models.IntegerField(
                                 blank=True,
                                 null=True,
                                 db_column="NUMBER_OF_EMI_PAID",
                             )
                             # Loan Lifecycle Dates
                             loan_disbursement_date = models.DateField(
                                 blank=False,
                                 null=False,
                                 db_column="LOAN_DISBURSEMENT_DATE",
                             )
                             maturity_date = models.DateField(
                                 blank=True,
                                 null=True,
                                 db_column="MATURITY_DATE",
                             )
                             emi_start_date = models.DateField(
                                 blank=True,
                                 null=True,
                                 db_column="EMI_START_DATE",
                             )
                             due_date = models.DateField(
                                 blank=False,
                                 null=False,
                                 db_column="DUE_DATE",
                             )
                             last_payment_date = models.DateField(
                                 blank=False,
                                 null=False,
                                 db_column="LAST_PAYMENT_DATE",
                             )
                             last_purchase_date = models.DateField(
                                 blank=True,
                                 null=True,
                                 db_column="LAST_PURCHASE_DATE",
                             )
                             mob = models.IntegerField(
                                 blank=True,
                                 null=True,
                                 db_column="MOB",
                             )
                             reason_of_bounce_date = models.DateField(
                                 blank=True,
                                 null=True,
                                 db_column="REASON_OF_BOUNCE_DATE",
                             )
                             # Payment History & Risk Profile
                             last_payment_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="LAST_PAYMENT_AMOUNT",
                             )
                             last_purchase_amount = models.DecimalField(
                                 max_digits=15,
                                 decimal_places=2,
                                 blank=False,
                                 null=False,
                                 db_column="LAST_PURCHASE_AMOUNT",
                             )
                             billing_cycle = models.CharField(
                                 max_length=50,
                                 blank=False,
                                 null=False,
                                 db_column="BILLING_CYCLE",
                             )
                             risk_statement = models.TextField(
                                 blank=True,
                                 null=True,
                                 db_column="RISK_STATEMENT",
                             )
                             delinquency_string = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="DELINQUENCY_STRING",
                             )
                             current_dpd = models.IntegerField(
                                 blank=False,
                                 null=False,
                                 db_column="CURRENT_DPD",
                             )
                         
                             allocation_type = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="ALLOCATION_TYPE",
                             )
                             nach_status = models.CharField(
                                 max_length=50,
                                 blank=True,
                                 null=True,
                                 db_column="NACH_STATUS",
                             )
                             reason_of_bounce = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="REASON_OF_BOUNCE",
                             )
                             # References
                             reference_name_1 = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="REFERENCE_NAME_1",
                             )
                             reference_contact_number_1 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="REFERENCE_CONTACT_NUMBER_1",
                             )
                             reference_name_2 = models.CharField(
                                 max_length=255,
                                 blank=True,
                                 null=True,
                                 db_column="REFERENCE_NAME_2",
                             )
                             reference_contact_number_2 = models.CharField(
                                 max_length=20,
                                 blank=True,
                                 null=True,
                                 db_column="REFERENCE_CONTACT_NUMBER_2",
                             )
                         
                             class Meta:
                                 db_table = "CASE_MANAGEMENT_TABLE"
                                
                         
                         class CaseManagementExtraFieldsModel(CoreGenericModel):
                             assigned_case = models.ForeignKey(
                                 CaseManagementCaseModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementExtraFieldsModel_assigned_case",
                                 blank=False,
                                 null=False,
                                 db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELDS_ID",
                             )
                             title = models.CharField(max_length=255, unique=True, db_column="EXTRA_FIELD_NAME")
                             data_type = models.CharField(
                                 max_length=255,
                                 choices=SQLDataTypeEnum.choices(),
                                 null=True,
                                 blank=True,
                                 db_column="EXTRA_FIELD_DATA_TYPE",
                             )
                         
                             class Meta:
                                 db_table = "CASE_MANAGEMENT_CASE_EXTRA_FIELDS_TABLE"
                                 # indexes = [
                                 #     models.Index(
                                 #         fields=["assigned_case"], name="idx_extra_fields_assigned_case"
                                 #     ),
                                 #     models.Index(fields=["title"], name="idx_extra_fields_title_case"),
                                 # ]
                         
                         
                         class CaseManagementExtraFieldDataModel(CoreGenericModel):
                             assigned_case = models.ForeignKey(
                                 CaseManagementCaseModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementExtraFieldDataModel_assigned_case",
                                 blank=False,
                                 null=False,
                                 db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELD_VALUE_ID",
                             )
                             title = models.OneToOneField(
                                 CaseManagementExtraFieldsModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementExtraFieldDataModel_title",
                                 unique=True,
                                 db_column="CASE_MANAGEMENT_CASE_EXTRA_FIELDS_ID",
                             )
                             value = models.CharField(
                                 max_length=1024, null=True, blank=True, db_column="EXTRA_FIELD_DATA"
                             )
                         
                             class Meta:
                                 db_table = "CASE_MANAGEMENT_CASE_EXTRA_FIELD_VALUE_TABLE"
                                 # indexes = [
                                 #     models.Index(fields=["assigned_case"], name="idx_ext_field_data_case"),
                                 #     models.Index(fields=["title"], name="idx_ext_field_title_case"),
                                 #     models.Index(fields=["value"], name="idx_ext_field_value_case"),
                                 # ]
                         
                         
                         class CaseManagementCaseAddressModel(CoreGenericModel):
                             assigned_case = models.ForeignKey(
                                 CaseManagementCaseModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseAddressModel_assigned_case",
                                 blank=False,
                                 null=False,
                                 db_column="CASE_MANAGEMENT_CASE_ADDRESS_ID",
                             )
                             address_type = models.ForeignKey(
                                 AddressTypeModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseModel_address_type",
                                 blank=False,
                                 null=False,
                                 db_column="ADDRESS_TYPE_ID",
                             )
                             address_1 = models.CharField(
                                 max_length=255,
                                 blank=False,
                                 null=False,
                                 db_column="ADDRESS_1",
                             )
                             address_2 = models.CharField(
                                 max_length=255,
                                 blank=False,
                                 null=False,
                                 db_column="ADDRESS_2",
                             )
                             address_3 = models.CharField(
                                 max_length=255,
                                 blank=False,
                                 null=False,
                                 db_column="ADDRESS_3",
                             )
                             address_4 = models.CharField(
                                 max_length=255,
                                 blank=False,
                                 null=False,
                                 db_column="ADDRESS_4",
                             )
                             city = models.CharField(
                                 max_length=100,
                                 blank=False,
                                 null=False,
                                 db_column="CUSTOMER_CITY",
                             )
                             region_config_city = models.ForeignKey(
                                 RegionConfigurationCityModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseAddressModel_region_config_city",
                                 blank=False,
                                 null=False,
                                 db_column="REGION_CONFIG_CUSTOMER_CITY",
                             )
                             pin_code = models.ForeignKey(
                                 RegionConfigurationPincodeModel,
                                 on_delete=models.CASCADE,
                                 related_name="CaseManagementCaseAddressModel_pin_code",
                                 blank=False,
                                 null=False,
                                 db_column="PIN_CODE_ID",
                             )
                             state = models.CharField(
                                 max_length=100,
                                 blank=False,
                                 null=False,
                                 db_column="CUSTOMER_STATE",
                             )
                             country = models.CharField(
                                 max_length=100,
                                 blank=False,
                                 null=False,
                                 db_column="COUNTRY",
                             )
                         
                             class Meta:
                                 db_table = "CASE_MANAGEMENT_CASE_ADDRESS_TABLE"
                         i want djanog orm questionon this around 200 question start from very easy beggineer level to expert level so if i pratice i will be master the orm queruies 
                 
         
