from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INVALID_STATUS_ERROR_MESSAGE,
    REGION_CONFIGRATION_ZONE_ALREADY_EXISTS,
    REGION_ID_NOT_FOUND_ERROR_MESSAGE,
    REGION_ID_REQUIRED,
    REGION_IS_NOT_ACTIVATED_ERROR_MESSAGE,
    REGION_IS_REQUIRED,
)
from store.configurations.region_config.models import (
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from typing import Optional


class RegionConfigurationZoneCreateHandler(CoreGenericBaseHandler):
    region_instance: RegionConfigurationRegionModel

    _activity_type: str = "CONFIGURATION_STATE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):

        region_uuid: Optional[str] = self.data.get("region")

        if self.queryset.filter(title__iexact=self.data["title"]).exists():
            return self.set_error_message(
                REGION_CONFIGRATION_ZONE_ALREADY_EXISTS,
                key="title",
            )

        if not self.data.get("region"):
            return self.set_error_message(REGION_IS_REQUIRED, key="region")

        if not region_uuid:
            return self.set_error_message(REGION_ID_REQUIRED, key="region")

        try:
            self.region_instance: RegionConfigurationRegionModel = (
                RegionConfigurationRegionModel.objects.get(pk=region_uuid)
            )

            if self.region_instance.status != "ACTIVATED":
                return self.set_error_message(
                    REGION_IS_NOT_ACTIVATED_ERROR_MESSAGE, key="region"
                )

        except RegionConfigurationRegionModel.DoesNotExist:
            return self.set_error_message(
                REGION_ID_NOT_FOUND_ERROR_MESSAGE, key="region"
            )

        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationZoneModel = self.queryset.create(
                region=self.region_instance,
                title=self.data["title"],
                description=self.data.get("description"),
            )
            self.update_core_generic_created_by(instance=instance)
            self.logger.info(
                f"Region Configuration created successfully. Region Configuration ID: {instance.pk}"
            )
