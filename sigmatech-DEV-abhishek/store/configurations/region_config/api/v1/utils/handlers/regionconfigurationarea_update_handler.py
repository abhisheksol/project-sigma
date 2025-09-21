from django.db import transaction
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    AREA_ID_NOT_FOUND,
    AREA_TITLE_ALREADY_EXISTS,
    INVALID_STATUS_ERROR_MESSAGE,
)
from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationPincodeModel,
)


class RegionConfigurationAreaUpdateHandler(CoreGenericBaseHandler):
    instance: RegionConfigurationAreaModel

    _activity_type: str = "CONFIGURATION_AREA_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    pincode_instance: RegionConfigurationPincodeModel | None = None

    def validate(self):
        # Ensure Area exists
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(AREA_ID_NOT_FOUND, key="id")

        # Validate pincode if provided
        pincode: int = self.data.get("pincode")
        if pincode:
            try:
                self.pincode_instance: RegionConfigurationPincodeModel = (
                    RegionConfigurationPincodeModel.objects.get(pk=pincode)
                )
            except RegionConfigurationPincodeModel.DoesNotExist:
                return self.set_error_message("Pincode ID not found", key="pincode")

        # Validate title if provided
        title = self.data.get("title")
        if title:
            if (
                self.queryset.filter(title__iexact=str(title).strip())
                .exclude(id=self.data["id"])
                .exists()
            ):
                return self.set_error_message(AREA_TITLE_ALREADY_EXISTS, key="title")

        # Validate status if provided
        status = self.data.get("status")
        if status and status not in list_enum_values(enum_cls=CoreUtilsStatusEnum):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationAreaModel = self.queryset.get(
                id=self.data["id"]
            )

            if self.pincode_instance:
                self.data["pincode"] = self.pincode_instance

            # Strip title if present
            if self.data.get("title"):
                self.data["title"] = str(self.data["title"]).strip()

            # This will handle status, title, pincode, etc.
            self.update_model_instance(instance=instance, data=self.data)

            self.set_toast_message_value(value=instance.title)
            self.logger.info(f"Area updated successfully. Area ID: {instance.pk}")
