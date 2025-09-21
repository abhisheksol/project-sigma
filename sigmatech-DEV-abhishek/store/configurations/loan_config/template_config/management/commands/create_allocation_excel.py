from django.core.management.base import BaseCommand

from typing import List
from core_utils.utils.enums import list_enum_values
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
    SQLDataTypeEnum,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
    ProcessTemplatePreferenceModel,
    SQLDataTypeModel,
)
from store.operations.case_management.global_variables import (
    all_possible_categorized_fields,
    template_required_fields,
)
from django.db.models.query import QuerySet
from django.db import transaction


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        all_possible_fields: List[str] = []
        for key in all_possible_categorized_fields.keys():
            all_possible_fields.extend(all_possible_categorized_fields[key])
        product_assignment_queryset: QuerySet[
            LoanConfigurationsProductAssignmentModel
        ] = LoanConfigurationsProductAssignmentModel.objects.all().exclude(
            pk="86bf4b6d-0cc9-468f-91d9-27eef486e0e4"
        )
        with transaction.atomic():
            for product_assignment_instance in product_assignment_queryset:
                template_preference_instance = ProcessTemplatePreferenceModel.objects.create(
                    title=f"{product_assignment_instance.product.title}_{product_assignment_instance.process.title}_static_file",
                    product_assignment=product_assignment_instance,
                )
                for all_possible_field in list_enum_values(
                    enum_cls=CustomAllocationFileTemplateReservedFieldsEnum
                ):
                    ProcessTemplateFieldMappingModel.objects.create(
                        template=template_preference_instance,
                        title=all_possible_field,
                        label=all_possible_field,
                        data_type=SQLDataTypeModel.objects.get(
                            title=(
                                SQLDataTypeEnum.DATE.value
                                if "date" in all_possible_field
                                else SQLDataTypeEnum.STRING.value
                            )
                        ),
                        preference_name=all_possible_field.upper(),
                        is_required_field=all_possible_field
                        in template_required_fields,
                    )
