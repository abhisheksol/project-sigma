from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    AREA_TITLE_ALREADY_EXISTS,
    AREA_TITLE_REQUIRED,
    INVALID_STATUS_ERROR_MESSAGE,
    PINCODE_ID_NOT_FOUND,
    PINCODE_IS_REQUIRED,
    PINCODE_NOT_BELONGS_TO_CITY,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationPincodeModel,
)
from typing import Union


class RegionConfigurationAreaCreateHandler(CoreGenericBaseHandler):
    pincode_instance: RegionConfigurationPincodeModel

    _activity_type: str = "CONFIGURATION_AREA_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):
        city_uuid: Union[str, None] = self.data.get("city")
        pincode_uuid: Union[str, None] = self.data.get("pincode")

        # Required fields check
        if not city_uuid:
            return self.set_error_message("CITY_ID is required", key="city")
        if not pincode_uuid:
            return self.set_error_message(PINCODE_IS_REQUIRED, key="pincode")
        if not self.data.get("title"):
            return self.set_error_message(AREA_TITLE_REQUIRED, key="title")

        # Unique title check
        if self.queryset.filter(title__iexact=str(self.data["title"]).strip()).exists():
            return self.set_error_message(AREA_TITLE_ALREADY_EXISTS, key="title")

        # Validate pincode exists
        try:
            self.pincode_instance = RegionConfigurationPincodeModel.objects.get(
                pk=pincode_uuid
            )
        except RegionConfigurationPincodeModel.DoesNotExist:
            return self.set_error_message(PINCODE_ID_NOT_FOUND, key="pincode")

        # Validate pincode belongs to the given city
        if str(self.pincode_instance.city_id) != str(city_uuid):
            return self.set_error_message(PINCODE_NOT_BELONGS_TO_CITY, key="pincode")

        # status validation
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationAreaModel = self.queryset.create(
                pincode=self.pincode_instance,
                title=self.data["title"].strip(),
            )
            self.update_core_generic_created_by(instance=instance)
            self.logger.info(f"Area created successfully. Area ID: {instance.pk}")
            return instance
