from typing import List
from django.core.management.base import BaseCommand
from pandas.core.frame import DataFrame
from core_utils.utils.file_utils.extract import fetch_dataframe_from_url
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from store.configurations.loan_config.template_config.management.utils.template_mapping import (
    TemplateMappingConfigUtils,
)
from django.db import transaction


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        template_url: str = (
            "https://objectstore.e2enetworks.net/sigmatech/4aa281db-320a-4134-a1b6-436ab0083fa1_allocation-file-template-mapping.xlsx"
        )

        print(
            f"Fetching Excel file for template mapping: {template_url}",
        )

        try:
            df: DataFrame = fetch_dataframe_from_url(template_url)
            print(
                f"Excel file loaded successfully with columns: {df.keys()}",
            )

            product_titles: List[str] = df.keys().drop("Field Name", errors="ignore")
            assignments = LoanConfigurationsProductAssignmentModel.objects.filter(
                product__title__in=product_titles
            )

            print(
                f"Found {assignments.count()} product assignments to process",
            )
            with transaction.atomic():
                for query in assignments:
                    print(
                        f"Processing product assignment: process={query.process.title}, product={query.product.title}",
                    )

                    TemplateMappingConfigUtils(
                        product_assignment_instance=query, template_url=template_url
                    ).assign_template_to_product_assignment()
                    print(
                        f"Successfully assigned template for product {query.product.title}",
                    )

            print("Template mapping process completed")

        except Exception as e:
            print("Failed to execute command:", str(e))
