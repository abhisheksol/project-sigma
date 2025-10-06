import django_filters
from ...models import UserConfigTableFieldsModel


class UserConfigGenericTableFieldsModelFilterSet(django_filters.FilterSet):
    class Meta:
        model = UserConfigTableFieldsModel
        fields = ["table__feature__title"]
