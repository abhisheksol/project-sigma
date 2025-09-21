import uuid
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel


# Create your models here.
class ReferalFileModel(CoreGenericModel):
    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid1,
        db_column="REFERAL_FILE_ID",
        editable=False,
    )
    title = models.CharField(max_length=255, unique=True, db_column="REFERAL_FILE_NAME")
    file_url = models.URLField(
        max_length=512, null=True, blank=True, db_column="FILE_URL"
    )
    latest_reupload_file_url = models.URLField(
        max_length=512, null=True, blank=True, db_column="LATEST_REUPLOAD_FILE_URL"
    )
    latest_error_file_url = models.URLField(
        max_length=512, null=True, blank=True, db_column="LATEST_ERROR_FILE_URL"
    )
    no_of_total_records = models.IntegerField(
        default=0, db_column="NO_OF_TOTAL_RECORDS"
    )
    no_of_valid_records = models.IntegerField(
        default=0, db_column="NO_OF_VALID_RECORDS"
    )
    no_of_error_records = models.IntegerField(
        default=0, db_column="NO_OF_ERROR_RECORDS"
    )
    no_of_duplicate_records = models.IntegerField(
        default=0, db_column="NO_OF_DUPLICATE_RECORDS"
    )

    class Meta:
        db_table = "REFERAL_FILE_TABLE"
