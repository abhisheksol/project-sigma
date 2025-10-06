from rest_framework import serializers
from core_utils.utils.generics.serializers.generic_serializers import (
    CoreGenericHelperAPISerializerMethodField,
)
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductsModel,
)


class LoanConfigurationsProcessHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):

    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsProcessModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class LoanConfigurationsProductHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):

    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsProductsModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class LoanConfigurationsMonthlyCycleHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):

    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsMonthlyCycleModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class LoanConfigurationsBucketHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="id", read_only=True)
    label = serializers.CharField(source="title", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsBucketModel
        fields = [
            "value",
            "label",
            "disabled",
        ]


class LoanConfigurationsBuckeRangeHelperModelSerializer(
    CoreGenericHelperAPISerializerMethodField, serializers.ModelSerializer
):
    value = serializers.UUIDField(source="id", read_only=True)
    disabled = serializers.SerializerMethodField()

    class Meta:
        model = BucketRangeModel
        fields = [
            "label",
            "value",
            "disabled",
        ]
