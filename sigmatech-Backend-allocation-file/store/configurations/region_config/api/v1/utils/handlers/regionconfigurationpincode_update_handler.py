from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.region_data.models import PincodeModel
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    PINCODE_ID_NOT_FOUND,
)
from store.configurations.region_config.api.v1.utils.handlers.regionconfigurationpincode_create_handler import (
    RegionConfigurationPincodeCreateHandler,
)
from django.db import transaction
from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
)
from store.configurations.region_config.api.v1.helper_apis.dependence import (
    can_edit_pincode,
)


class RegionConfigurationPincodeUpdateHandler(RegionConfigurationPincodeCreateHandler):

    _activity_type: str = "CONFIGURATION_PINCODE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.UPDATE.value

    city_instance: RegionConfigurationCityModel
    pincode_instance: RegionConfigurationPincodeModel

    def validate(self):
        # ID NOT FOUND
        if not self.queryset.filter(id=self.data["id"]).exists():
            return self.set_error_message(PINCODE_ID_NOT_FOUND, key="id")

        # getting pincode instance

        if self.data.get("id"):
            try:
                self.instance: RegionConfigurationPincodeModel = self.queryset.get(
                    id=self.data["id"]
                )
            except RegionConfigurationPincodeModel.DoesNotExist:
                return self.set_error_message(PINCODE_ID_NOT_FOUND, key="id")

        if "city" in self.data:
            try:
                self.city_instance: RegionConfigurationCityModel = (
                    RegionConfigurationCityModel.objects.get(pk=self.data["city"])
                )
            except RegionConfigurationCityModel.DoesNotExist:
                return self.set_error_message("City ID not found", key="city")

        # todo add constant
        if "pincode" in self.data:
            try:
                self.pincode_instance: PincodeModel = PincodeModel.objects.get(
                    pincode=self.data["pincode"]
                )
            except PincodeModel.DoesNotExist:
                return self.set_error_message("Pincode ID not found", key="pincode")

        # todo add constant
        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message("Invalid status", key="status")

        # -------------------------------------------------

        error = can_edit_pincode(self.instance)
        if error:
            return self.set_error_message(error, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationPincodeModel = self.queryset.get(
                id=self.data["id"]
            )

            if "city" in self.data:
                instance.city = self.city_instance  # assign FK relation
                self.data.pop("city")

            if "pincode" in self.data:
                instance.pincode = self.pincode_instance  # assign FK relation
                self.data.pop("pincode")

            self.set_toast_message_value(value=instance.pincode.pincode)

            self.update_model_instance(instance=instance, data=self.data)
            self.logger.info(
                f"Region Configuration updated successfully. Region Configuration ID: {instance.pk}"
            )
