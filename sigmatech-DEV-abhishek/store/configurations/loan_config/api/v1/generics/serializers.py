from rest_framework import serializers
from store.configurations.loan_config.api.v1.utils.handlers.bucketcycle_Update_handler import (
    BucketUpdateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.bucketcycle_create_handler import (
    BucketCreateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.monthlycycle_create_handler import (
    MonthlyCycleCreateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.monthlycycle_update_handler import (
    MonthlyCycleUpdateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.process_create_handler import (
    ProcessCreateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.process_update_handler import (
    ProcessUpdateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.product_create_handler import (
    ProductCreateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.product_update_handler import (
    ProductUpdateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.productassignment_create_handler import (
    ProductAssignmentCreateHandler,
)
from store.configurations.loan_config.api.v1.utils.handlers.productassignment_update_handler import (
    ProductAssignmentUpdateHandler,
)
from store.configurations.loan_config.models import (
    BucketRangeModel,
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)

from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin

from django.db.models.query import QuerySet

# --------------------------------------Process List Serializer ------------------------------------------


class LoanConfigurationsProcessListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = ProcessCreateHandler
    products = serializers.SerializerMethodField()

    class Meta:
        model = LoanConfigurationsProcessModel
        fields = [
            "id",
            "title",
            "logo",
            "status",
            "contact_person_name",
            "contact_person_email",
            "contact_person_phone_number",
            "products",
            "status",
        ]

    def get_products(self, obj) -> list:
        try:
            products_assigned_queryset: QuerySet[
                LoanConfigurationsProductAssignmentModel
            ] = obj.LoanConfigurationsProductAssignmentModel_process.all()
            product_title_list: list = products_assigned_queryset.values_list(
                "product__title", flat=True
            )
            return product_title_list
        except Exception as e:
            self.context["logger"].error(str(e))
            return []


class LoanConfigurationsProcessCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = ProcessCreateHandler

    class Meta:
        model = LoanConfigurationsProcessModel
        fields = [
            "title",
            "logo",
            "contact_person_name",
            "contact_person_email",
            "contact_person_phone_number",
        ]


class LoanConfigurationsProcessPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = ProcessUpdateHandler
    id = serializers.UUIDField()
    title = serializers.CharField(required=False)
    logo = serializers.URLField(required=False)
    status = serializers.CharField(required=False)
    contact_person_name = serializers.CharField(required=False)
    contact_person_email = serializers.EmailField(required=False)
    contact_person_phone_number = serializers.CharField(required=False)
    queryset = LoanConfigurationsProcessModel.objects.all()


# -------------------------------------Product Model Serializer-------------------------------------


class LoanConfigurationsProductListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = ProductCreateHandler

    class Meta:
        model = LoanConfigurationsProductsModel
        fields = [
            "id",
            "title",
            "status",
            "description",
        ]


class LoanConfigurationsProductCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = ProductCreateHandler

    class Meta:
        model = LoanConfigurationsProductsModel
        fields = ["title", "description"]


class LoanConfigurationsProductPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = ProductUpdateHandler
    id = serializers.UUIDField()
    title = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    queryset = LoanConfigurationsProductsModel.objects.all()


# -------------------------------------Monthly Cycle  Serializer-------------------------------------


class LoanConfigurationsMonthlyCycleListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = MonthlyCycleCreateHandler

    class Meta:
        model = LoanConfigurationsMonthlyCycleModel
        fields = [
            "id",
            "title",
            "status",
            "description",
        ]


class LoanConfigurationsMonthlyCycleCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = MonthlyCycleCreateHandler

    class Meta:
        model = LoanConfigurationsMonthlyCycleModel
        fields = [
            "title",
            "status",
            "description",
        ]


class LoanConfigurationsMonthlyCyclePutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = MonthlyCycleUpdateHandler
    id = serializers.UUIDField()
    title = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    queryset = LoanConfigurationsMonthlyCycleModel.objects.all()


# -------------------------------------Bucket List Serializer-------------------------------------


class LoanConfigurationsBucketListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):

    handler_class = BucketCreateHandler
    range__label = serializers.CharField(source="range.label", read_only=True)
    # range_id
    range = serializers.UUIDField(source="range.id", read_only=True)

    class Meta:
        model = LoanConfigurationsBucketModel
        fields = [
            "id",
            "title",
            "description",
            "range__label",
            "range",
            "status",
        ]


class LoanConfigurationsBucketCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    handler_class = BucketCreateHandler
    range = serializers.UUIDField()

    class Meta:
        model = LoanConfigurationsBucketModel
        fields = [
            "title",
            "description",
            "range",
            "status",
        ]


class LoanConfigurationsBucketPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = BucketUpdateHandler
    id = serializers.UUIDField()
    range = serializers.UUIDField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    queryset = LoanConfigurationsBucketModel.objects.all()


# -------------------------------------Product Assignment Serializer-------------------------------------


class LoanConfigurationsProductAssignmentListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    product__title = serializers.CharField(
        source="product.title", allow_blank=True, default=None
    )
    handler_class = ProductAssignmentCreateHandler

    class Meta:
        model = LoanConfigurationsProductAssignmentModel
        fields = [
            "id",
            "process",
            "product",
            "product__title",
            "min_due_percentage",
            "refer_back_percentage",
            "status",
        ]


class LoanConfigurationsProductAssignmentCreateModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):
    process = serializers.UUIDField()
    product = serializers.UUIDField()
    min_due_percentage = serializers.FloatField(required=False)
    refer_back_percentage = serializers.FloatField(required=False)
    handler_class = ProductAssignmentCreateHandler

    class Meta:
        model = LoanConfigurationsProductAssignmentModel
        fields = [
            "process",
            "product",
            "min_due_percentage",
            "refer_back_percentage",
        ]


class LoanConfigurationsProductAssignmentPutSerializer(
    CoreGenericSerializerMixin, serializers.Serializer
):
    handler_class = ProductAssignmentUpdateHandler
    id = serializers.UUIDField()
    process = serializers.UUIDField(required=False)
    product = serializers.UUIDField(required=False)
    status = serializers.CharField(required=False)
    min_due_percentage = serializers.FloatField(required=False)
    refer_back_percentage = serializers.FloatField(required=False)
    queryset = LoanConfigurationsProductAssignmentModel.objects.all()


class LoanConfigurationsProcessDetailModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanConfigurationsProcessModel
        fields = ["id", "logo", "status", "title"]


# -------------------------------------Bucket Range List Serializer-------------------------------------
class LoanConfigurationsBucketRangeListModelSerializer(
    CoreGenericSerializerMixin, serializers.ModelSerializer
):

    class Meta:
        model = BucketRangeModel
        fields = ["id", "label", "value"]
