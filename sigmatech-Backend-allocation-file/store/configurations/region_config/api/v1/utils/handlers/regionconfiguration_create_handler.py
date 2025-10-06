from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import CoreUtilsStatusEnum, list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
from store.configurations.region_config.api.v1.utils.handlers.constants import (
    INVALID_STATUS_ERROR_MESSAGE,
    REGION_ALREADY_EXISTS,
    REGION_DESCRIPTION_LENGTH_ERROR_MESSAGE,
    REGION_IS_REQUIRED,
    REGION_TITLE_LENGTH_ERROR_MESSAGE,
)
from store.configurations.region_config.models import RegionConfigurationRegionModel


class RegionCOnfigurationCreateHandler(CoreGenericBaseHandler):

    _activity_type: str = "CONFIGURATION_REGION_ACTIVITY_LOG"
    _method: str = ActivityMonitoringMethodTypeEnumChoices.CREATE.value

    def validate(self):

        # check the length of title and description

        if len(self.data["title"]) > 50:
            return self.set_error_message(
                REGION_TITLE_LENGTH_ERROR_MESSAGE, key="title"
            )

        if len(self.data["description"]) > 100:
            return self.set_error_message(
                REGION_DESCRIPTION_LENGTH_ERROR_MESSAGE, key="description"
            )

        # REGION IS REQUIRED
        if not self.data.get("title"):
            return self.set_error_message(REGION_IS_REQUIRED, key="title")

        # region exists case validation
        if self.queryset.filter(title__iexact=self.data["title"]).exists():
            return self.set_error_message(REGION_ALREADY_EXISTS, key="title")

        if self.data.get("status") and self.data.get("status") not in list_enum_values(
            enum_cls=CoreUtilsStatusEnum
        ):
            return self.set_error_message(INVALID_STATUS_ERROR_MESSAGE, key="status")

    def create(self):
        with transaction.atomic():
            instance: RegionConfigurationRegionModel = self.queryset.create(**self.data)
            self.update_core_generic_created_by(instance=instance)

            self.logger.info(
                f"Region Configuration created successfully. Region Configuration ID: {instance.pk}"
            )
