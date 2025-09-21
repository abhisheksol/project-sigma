from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    CITY_NAME_ALREADY_EXISTS,
    CITY_NAME_REQUIRED,
    INVALID_STATUS_ERROR_MESSAGE,
    ZONE_ID_NOT_FOUND,
    ZONE_ID_REQUIRED,
)
from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationZoneModel,
)
from typing import Union


class RegionConfigurationCityCreateHandler(CoreGenericBaseHandler):
    zone_instance: Union[RegionConfigurationZoneModel, None] = None

    _activity_type: str = "CONFIGURATION_CITY_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):
        zone_uuid: Union[str, None] = self.data.get("zone")
        city_name: Union[str, None] = self.data.get("city_name")

        # check zone id
        if not zone_uuid:
            return self.set_error_message(ZONE_ID_REQUIRED, key="zone")

        # check city name
        if not city_name:
            return self.set_error_message(CITY_NAME_REQUIRED, key="city_name")

        #  validate zone exists
        try:
            self.zone_instance: RegionConfigurationZoneModel = (
                RegionConfigurationZoneModel.objects.get(pk=zone_uuid)
            )
        except RegionConfigurationZoneModel.DoesNotExist:
            return self.set_error_message(ZONE_ID_NOT_FOUND, key="zone")

        if self.queryset.filter(
            zone=self.zone_instance, city_name__iexact=city_name.strip()
        ).exists():
            return self.set_error_message(CITY_NAME_ALREADY_EXISTS, key="city_name")

        # todo add constant
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationCityModel = self.queryset.create(
                zone=self.zone_instance,
                city_name=self.data.get("city_name").strip(),
                description=self.data.get("description"),
            )
            self.set_toast_message_value(value=instance.city_name)
            self.update_core_generic_created_by(instance=instance)
            self.logger.info(f"City created successfully. ID: {instance.pk}")
            return instance
