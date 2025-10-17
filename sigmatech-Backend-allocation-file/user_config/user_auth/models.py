from django.db import models
import uuid

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

    class Meta:
        db_table = "USER_ROLE_TABLE"


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
        db_table = "USER_LOGIN_ANALYTICS_TABLE"


class MobileOTPModel(CoreGenericModel):
    id = models.UUIDField(
        db_column="MOBILE_OTP_ID",
        default=uuid.uuid1,
        unique=True,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="MobileOTPModel_user",
        db_column="USER_ID",
    )
    mobile_otp = models.CharField(max_length=6, db_column="MOBILE_OTP")
    is_expired = models.BooleanField(default=False, db_column="IS_EXPIRED")

    class Meta:
        db_table = "MOBILE_OTP_TABLE"


from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
from user_config.user_auth.models import UserModel
# ...existing code...
from enum import Enum

class FoStatusenum(Enum):
    ON_DUTY = "ON_DUTY"
    OFF_DUTY = "OFF_DUTY"

    @classmethod
    def choices(cls):
        return [(member.value, member.name.replace("_", " ").title()) for member in cls]
# ...existing code...

 
class FoAttendanceModel(CoreGenericModel):
    fo_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        db_column="FO_USER_ID",
    )
    date = models.DateField(
        db_column="DATE"
    )
    duty_on = models.TimeField(
        null=True,
        blank=True,
        db_column="DUTY_ON",
    )
    duty_off = models.TimeField(
        null=True,
        blank=True,
        db_column="DUTY_OFF",
    )
 
    fo_status = models.CharField(
        max_length=20,
        default=FoStatusenum.OFF_DUTY.value,
        db_column="FO_STATUS",
        choices=FoStatusenum.choices(),
    )
 
    class Meta:
        db_table = "FO_ATTENDANCE_TABLE"
        indexes = [
            models.Index(fields=["fo_user"]),
            models.Index(fields=["date"]),
        ]
 
    def __str__(self):
        return f"{self.fo_user.username} - {self.date}"
 