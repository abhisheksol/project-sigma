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
        unique_together = ("permission", "user")
