import django_filters

from store.configurations.loan_config.models import (
    LoanConfigurationsBucketModel,
    LoanConfigurationsMonthlyCycleModel,
    LoanConfigurationsProcessModel,
    LoanConfigurationsProductAssignmentModel,
    LoanConfigurationsProductsModel,
)


class ProcessFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = LoanConfigurationsProcessModel
        fields = ["title", "status"]


class ProductFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    code = django_filters.CharFilter(field_name="code", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = LoanConfigurationsProductsModel
        fields = ["title", "code", "status"]


class MonthlyCycleFilterSet(django_filters.FilterSet):
    title = django_filters.NumberFilter(field_name="title", lookup_expr="exact")

    class Meta:
        model = LoanConfigurationsMonthlyCycleModel
        fields = ["title"]


class BucketFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = LoanConfigurationsBucketModel
        fields = ["title"]


# Product Assignment filter


class ProductAssignmentFilterSet(django_filters.FilterSet):
    # product search by title (works because it's CharField)
    title = django_filters.CharFilter(
        field_name="product__title",
        lookup_expr="icontains",
    )

    # process filtering (ForeignKey – use exact match)
    process = django_filters.CharFilter(
        field_name="process",
        lookup_expr="exact",
    )

    class Meta:
        model = LoanConfigurationsProductAssignmentModel
        fields = ["title", "process"]
