from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    CITY_ID_NOT_FOUND,
    CITY_ID_REQUIRED,
    CITY_NOT_BELONGS_TO_ZONE,
    INVALID_PINCODES_ERROR_MESSAGE,
    INVALID_STATUS_ERROR_MESSAGE,
    PINCODE_ALREADY_EXISTS_ERROR_MESSAGE,
    PINCODE_IS_REQUIRED,
    ZONE_ID_NOT_FOUND,
    ZONE_ID_REQUIRED,
)
from store.configurations.region_config.models import (
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationZoneModel,
)
from typing import Union, List
from core_utils.region_data.models import PincodeModel


class RegionConfigurationPincodeCreateHandler(CoreGenericBaseHandler):

    _activity_type: str = "CONFIGURATION_PINCODE_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    city_instance: RegionConfigurationCityModel
    zone_instance: RegionConfigurationZoneModel
    valid_pincodes: list

    def validate(self):
        zone_uuid: Union[str, None] = self.data.get("zone")
        city_uuid: Union[str, None] = self.data.get("city")
        pincode_list: List[int] = self.data.get("pincode", [])

        # Pincode non-empty check
        if not pincode_list:
            return self.set_error_message(PINCODE_IS_REQUIRED, key="pincode")

        # todo add constant
        # Zone check
        if not zone_uuid:
            return self.set_error_message(ZONE_ID_REQUIRED, key="zone")
        try:
            self.zone_instance: RegionConfigurationZoneModel = (
                RegionConfigurationZoneModel.objects.get(pk=zone_uuid)
            )
        except RegionConfigurationZoneModel.DoesNotExist:
            return self.set_error_message(ZONE_ID_NOT_FOUND, key="zone")

        # City check
        if not city_uuid:
            return self.set_error_message(CITY_ID_REQUIRED, key="city")
        try:
            self.city_instance: RegionConfigurationCityModel = (
                RegionConfigurationCityModel.objects.get(pk=city_uuid)
            )
        except RegionConfigurationCityModel.DoesNotExist:
            return self.set_error_message(CITY_ID_NOT_FOUND, key="city")

        # Check if city belongs to zone
        if self.city_instance.zone_id != self.zone_instance.id:
            return self.set_error_message(CITY_NOT_BELONGS_TO_ZONE, key="city")

        # Validate pincodes
        invalid_pincodes: List[int] = []
        self.valid_pincodes: List[int] = []
        for pin in pincode_list:
            try:
                pincode_instance: PincodeModel = PincodeModel.objects.get(pincode=pin)

                # Validate pincode already exists
                if self.queryset.filter(pincode=pincode_instance).exists():
                    return self.set_error_message(
                        PINCODE_ALREADY_EXISTS_ERROR_MESSAGE, key="pincode"
                    )

                self.valid_pincodes.append(pincode_instance)
            except PincodeModel.DoesNotExist:
                invalid_pincodes.append(pin)

        if invalid_pincodes:
            return self.set_error_message(
                INVALID_PINCODES_ERROR_MESSAGE.format(pincodes=invalid_pincodes),
                key="pincode",
            )

        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        created_instance: List[RegionConfigurationPincodeModel] = []
        with transaction.atomic():
            for pincode_instance in self.valid_pincodes:
                instance: RegionConfigurationPincodeModel = self.queryset.create(
                    pincode=pincode_instance,
                    city=self.city_instance,
                )
                created_instance.append(instance)

            self.set_toast_message_value(
                value=", ".join([str(obj.pincode.pincode) for obj in created_instance])
            )

            self.update_core_generic_created_by(instance=instance)

            self.logger.info(
                f"Pincode(s) created successfully. IDs: {str([str(obj.id) for obj in created_instance])}"
            )
