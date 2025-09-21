from django.contrib.auth import get_user_model
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid

# Create your models here.


class CoreUtilsMediaUrlModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="MEDIA_URL_ID",
        editable=False,
    )
    file_name = models.CharField(
        max_length=500, null=True, blank=True, db_column="FILE_NAME"
    )
    file_type = models.CharField(
        max_length=255, null=True, blank=True, db_column="FILE_TYPE"
    )  # file extension
    file_size = models.CharField(
        max_length=255, null=True, blank=True, db_column="FILE_SIZE"
    )
    media_url = models.URLField(
        max_length=1000, unique=True, null=True, blank=True, db_column="MEDIA_URL"
    )

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="CoreUtilsMediaUrlModel_created_by",
        db_column="CREATED_BY",
    )

    class Meta:
        ordering = ("-core_generic_created_at",)
        db_table = "MEDIA_URL_TABLE"


class CoreUtilsE2EMediaStorageModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="MEDIA_URL_ID",
        editable=False,
    )

    # Original uploaded file name
    file_name = models.CharField(
        max_length=500, null=True, blank=True, db_column="FILE_NAME"
    )

    # File extension/type
    file_type = models.CharField(
        max_length=50, null=True, blank=True, db_column="FILE_TYPE"
    )

    # Size in bytes
    file_size = models.BigIntegerField(null=True, blank=True, db_column="FILE_SIZE")

    # Bucket name in E2E object store
    bucket_name = models.CharField(
        max_length=255, null=True, blank=True, db_column="BUCKET_NAME"
    )

    # Path where file was read from (temporary local file)
    source_file = models.TextField(null=True, blank=True, db_column="SOURCE_FILE")

    # Key/object name inside MinIO
    destination_file = models.TextField(
        null=True, blank=True, db_column="DESTINATION_FILE"
    )

    # Permanent URL (public link or reverse-proxy endpoint)
    permanent_url = models.TextField(null=True, blank=True, db_column="PERMANENT_URL")

    storage_url = models.TextField(
        null=True, blank=True, db_column="E2E_BLOB_STORAGE_URL"
    )

    class Meta:
        ordering = ("-core_generic_created_at",)
        db_table = "E2E_MEDIA_URL_TABLE"
