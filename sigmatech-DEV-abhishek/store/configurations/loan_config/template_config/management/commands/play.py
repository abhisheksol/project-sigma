from django.core.management.base import BaseCommand

from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        order: int = 1
        for query in ProcessTemplateFieldMappingModel.objects.all():
            print(query.title, query.label)
            query.label = query.label.upper()
            query.ordering = order
            order += 1

            query.save()
