from django.core.management.base import BaseCommand
from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
    ProcessTemplateMultiReferenceFieldModel,
)


class Command(BaseCommand):
    help: str = "Playground Shell"

    def handle(self, *args, **kwargs):
        outputdata: list = []
        for instance in ProcessTemplateFieldMappingModel.objects.all():
            tempinstance: dict = {
                **ProcessTemplateFieldMappingModel.objects.filter(
                    pk=instance.pk
                ).values("title", "label")[0]
            }

            if instance.is_multi_ref_field:

                tempinstance["multi_ref_field"] = (
                    ProcessTemplateMultiReferenceFieldModel.objects.filter(
                        reference_field=instance
                    ).values("title", "label")
                )
            outputdata.append(tempinstance)

        print("outputdata", outputdata)
