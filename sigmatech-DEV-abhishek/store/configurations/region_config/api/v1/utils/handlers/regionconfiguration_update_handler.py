from django.db import transaction


from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INVALID_STATUS_ERROR_MESSAGE,
    REGION_ALREADY_EXISTS,
    REGION_CONFIGRATION_ID_NOT_FOUND,
    REGION_CONFIGRATION_ID_REQUIRED,
)
from store.configurations.region_config.models import RegionConfigurationRegionModel


class RegionConfigurationUpdateHandler(CoreGenericBaseHandler):

    _activity_type: str = "CONFIGURATION_REGION_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):

        if not self.data.get("id"):
            return self.set_error_message(REGION_CONFIGRATION_ID_REQUIRED, key="id")

        try:
            self.instance = RegionConfigurationRegionModel.objects.get(
                id=self.data["id"]
            )
        except RegionConfigurationRegionModel.DoesNotExist:
            return self.set_error_message(REGION_CONFIGRATION_ID_NOT_FOUND, key="id")

        if (
            self.data.get("title")
            and self.queryset.filter(title__iexact=self.data["title"]).exists()
        ):
            return self.set_error_message(REGION_ALREADY_EXISTS, key="title")

        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():

            self.update_model_instance(instance=self.instance, data=self.data)
            self.logger.info(
                f"Region Configuration updated successfully. Region Configuration ID: {self.instance.pk}"
            )
