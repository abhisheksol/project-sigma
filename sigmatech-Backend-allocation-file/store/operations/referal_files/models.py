import uuid
from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel

from user_config.user_auth.models import UserModel
# Remove this import:
# from store.operations.case_management.models import CaseManagementCaseModel
from store.configurations.region_config.models import RegionConfigurationPincodeModel, RegionConfigurationAreaModel

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



class FieldOfficerAssignment(CoreGenericModel):
    """
    Stores mapping of Field Officers to pin codes and sub-areas.
    All derived values like assigned cases, POS, upcoming visits will be
    calculated dynamically when requested.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False,
        db_column="FO_ASSIGNMENT_ID",
    )

    # The FO (Field Officer) user
    field_officer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        limit_choices_to={"user_role__role": "FIELD_OFFICER"},
        related_name="fo_assignments",
    )

    # Pin codes assigned to FO
    assigned_pincodes = models.ManyToManyField(
        RegionConfigurationPincodeModel,
        blank=True,
        related_name="fo_assigned_pincodes",
    )

    # Sub-areas assigned to FO
    assigned_sub_areas = models.ManyToManyField(
        RegionConfigurationAreaModel,
        blank=True,
        related_name="fo_assigned_areas",
    )

    # FO Status
    is_active = models.BooleanField(default=True)
    on_duty = models.BooleanField(default=True)

    # Optional: next planned visit (can be updated dynamically if needed)
    upcoming_visit_date = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "FO_ASSIGNMENT_TABLE"

    def __str__(self):
        return f"FO: {self.field_officer.username}"