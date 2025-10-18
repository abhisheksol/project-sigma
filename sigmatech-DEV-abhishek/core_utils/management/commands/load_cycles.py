from django.core.management.base import BaseCommand
from typing import List

from store.configurations.loan_config.models import LoanConfigurationsMonthlyCycleModel


class Command(BaseCommand):
    help: str = "Playground Shell"

    def handle(self, *args, **kwargs):
        cycle_list: List[int] = [i for i in range(1, 32)] + [99]
        print("loading cycles", cycle_list)
        for cycle in cycle_list:
            LoanConfigurationsMonthlyCycleModel.objects.create(title=cycle)

        print("Cycle loadded successfully")
