from typing import Union
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationZoneModel,
)
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    CITY_ID_NOT_FOUND,
    CITY_ID_REQUIRED,
    CITY_NAME_ALREADY_EXISTS,
    INVALID_STATUS_ERROR_MESSAGE,
    ZONE_ID_NOT_FOUND,
)
from store.configurations.region_config.api.v1.helper_apis.dependence import (
    can_edit_city,
)


class RegionConfigurationCityUpdateHandler(CoreGenericBaseHandler):
    _activity_type: str = "CONFIGURATION_CITY_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    instance: RegionConfigurationCityModel
    zone_instance: Union[RegionConfigurationZoneModel, None] = None

    def validate(self):
        # check ID
        if not self.data.get("id"):
            return self.set_error_message(CITY_ID_REQUIRED, key="id")

        try:
            self.instance: RegionConfigurationCityModel = self.queryset.get(
                id=self.data["id"]
            )
        except RegionConfigurationCityModel.DoesNotExist:
            return self.set_error_message(CITY_ID_NOT_FOUND, key="id")

        # check zone (if provided)
        if "zone" in self.data:
            try:
                self.zone_instance = RegionConfigurationZoneModel.objects.get(
                    pk=self.data["zone"]
                )
            except RegionConfigurationZoneModel.DoesNotExist:
                return self.set_error_message(ZONE_ID_NOT_FOUND, key="zone")

        # check city_name (if provided)
        if self.data.get("city_name"):
            city_name = str(self.data.get("city_name")).strip()

            if (
                self.queryset.filter(
                    zone=self.zone_instance or self.instance.zone,
                    city_name__iexact=city_name,
                )
                .exclude(id=self.instance.id)
                .exists()
            ):
                return self.set_error_message(CITY_NAME_ALREADY_EXISTS, key="city_name")

        # check status
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

        # ----------------------------------

        error = can_edit_city(self.instance)
        if error:
            return self.set_error_message(error, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationCityModel = self.instance

            if self.data.get("city_name"):
                instance.city_name = str(self.data["city_name"]).strip()

            if self.zone_instance:

                instance.zone = self.zone_instance
                self.data.pop("zone")

            self.set_toast_message_value(value=instance.city_name)
            self.update_model_instance(instance=instance, data=self.data)

            self.logger.info(f"City updated successfully. City ID: {instance.pk}")
