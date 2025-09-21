from rest_framework import serializers


class AllocationFileStatusListHelperModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    @classmethod
    def get_dropdown_data(cls):
        return [
            {"label": "INPROCESS", "value": "In Process"},
            {"label": "EXPIRED", "value": "Expired"},
            {"label": "COMPLETED", "value": "Completed"},
        ]

    def to_representation(self, instance):
        return instance
