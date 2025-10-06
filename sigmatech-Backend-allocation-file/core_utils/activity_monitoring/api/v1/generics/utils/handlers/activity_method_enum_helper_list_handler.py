from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.utils.enums import list_enum_values
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from typing import List


class ActivityMethodEnumHelperListEnumHandler(CoreGenericBaseHandler):

    def validate(self):
        return

    def create(self):
        results: List[str] = []
        enum_data = list_enum_values(enum_cls=ActivityMonitoringMethodTypeEnumChoices)
        for enum in enum_data:
            results.append({"value": enum, "label": enum})
        self.data["results"] = results
