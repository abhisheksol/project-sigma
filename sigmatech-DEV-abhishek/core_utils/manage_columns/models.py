from django.db import models

from core_utils.utils.generics.generic_models import CoreGenericModel

from django.contrib.auth import get_user_model

# Create your models here.


class CoreUtilsFeaturesModel(CoreGenericModel):
    id = models.BigAutoField(db_column="ID", unique=True, primary_key=True)
    title = models.CharField(max_length=255, unique=True, db_column="FEATURE_TITLE")

    model_name = models.CharField(max_length=511, null=True, db_column="ORM_MODEL_NAME")
    view_name = models.CharField(
        max_length=511, null=True, db_column="DJANGO_VIEW_NAME"
    )
    serializer = models.CharField(max_length=511, db_column="DJANGO_SERIALIZER_NAME")
    is_active = models.BooleanField(default=True, db_column="IS_ACTIVE")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-core_generic_created_at",)
        db_table = "APPLICATION_FEATURE_TABLE"


class UserConfigTableOrderModel(CoreGenericModel):
    id = models.BigAutoField(db_column="ID", unique=True, primary_key=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="UserPreferenceTableOrderModel_user",
        db_column="PERSON",
    )
    feature = models.ForeignKey(
        CoreUtilsFeaturesModel,
        on_delete=models.CASCADE,
        related_name="UserPreferenceTableOrderModel_feature",
        db_column="APPLICATION_FEATURE",
    )
    pagination_size = models.IntegerField(default=10, db_column="PAGINATION_COUNT")
    is_default = models.BooleanField(default=True, db_column="IS_DEFAULT")

    class Meta:
        unique_together = ("user", "feature")
        db_table = "USER_CONFIG_TABLE_ORDER_TABLE"


class UserConfigTableFieldsModel(CoreGenericModel):
    id = models.BigAutoField(db_column="ID", unique=True, primary_key=True)
    title = models.CharField(max_length=255, db_column="TITLE")
    order = models.IntegerField(db_column="ORDER")
    table = models.ForeignKey(
        UserConfigTableOrderModel,
        on_delete=models.CASCADE,
        related_name="UserPreferenceTableFieldsModel_table",
        db_column="TABLE",
    )
    is_active = models.BooleanField(default=True, db_column="IS_ACTIVE")

    class Meta:
        unique_together = ("title", "table")
        db_table = "USER_CONFIG_TABLE_ORER_FIELDS_TABLE"
