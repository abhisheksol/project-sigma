from copy import deepcopy
from typing import Optional, Dict

from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INCORRECT_ZONE_ID,
    INVALID_STATUS_ERROR_MESSAGE,
    REGION_CONFIGRATION_ID_NOT_FOUND,
)
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from store.configurations.region_config.api.v1.helper_apis.dependence import (
    can_edit_zone,
)


class RegionConfigurationZoneUpdateHandler(CoreGenericBaseHandler):
    region_instance: Optional[RegionConfigurationRegionModel] = None
    instance: RegionConfigurationZoneModel

    _activity_type: str = "CONFIGURATION_STATE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    def validate(self):

        region_uuid: Optional[str] = self.data.get("region")

        try:
            self.instance: RegionConfigurationZoneModel = self.queryset.get(
                pk=self.data["id"]
            )
        except RegionConfigurationZoneModel.DoesNotExist:
            return self.set_error_message(INCORRECT_ZONE_ID, key="id")

        try:
            if region_uuid:
                self.region_instance: RegionConfigurationRegionModel = (
                    RegionConfigurationRegionModel.objects.get(pk=region_uuid)
                )

        except RegionConfigurationRegionModel.DoesNotExist:
            return self.set_error_message(
                REGION_CONFIGRATION_ID_NOT_FOUND, key="region"
            )

        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

        # -------------------------------------------------

        error = can_edit_zone(self.instance)
        if error:
            return self.set_error_message(error, key="status")

    def create(self):

        with transaction.atomic():
            data: Dict = deepcopy(self.data)

            if self.region_instance:
                data["region"] = self.region_instance

            self.instance: RegionConfigurationZoneModel = self.update_model_instance(
                instance=self.instance, data=data
            )

            self.logger.info(
                f"Region Configuration updated successfully. Region Configuration ID: {self.instance.pk}"
            )
