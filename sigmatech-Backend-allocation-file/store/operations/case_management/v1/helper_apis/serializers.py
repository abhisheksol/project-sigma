from rest_framework import serializers

from store.operations.case_management.enums import CaseLifecycleStageEnum

enum_list = {"CaseLifecycleStageEnum": CaseLifecycleStageEnum}


class CaseALLocationRiskListHelperModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    @classmethod
    def get_dropdown_data(cls):
        return [
            {"label": "HIGH", "value": "HIGH"},
            {"label": "MEDIUM", "value": "MEDIUM"},
            {"label": "LOW", "value": "LOW"},
            {"label": "CRITICAL", "value": "CRITICAL"},
        ]

    def to_representation(self, instance):
        return instance
