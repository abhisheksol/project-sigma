from django.core.management.base import BaseCommand

from store.operations.allocation_files.v1.upload.utils.save.allocation_file_save_sub_areas import (
    save_sub_area_to_allocation_case_instance,
)
from store.operations.case_management.models import CaseManagementCaseModel


# F8X8+QP8, Kailash Nagar, Chanda Nagar, Ramachandrapuram, Hyderabad, Telangana 502032


class Command(BaseCommand):
    help: str = "Playground Shell"

    def handle(self, *args, **kwargs):
        # case_instance : CaseManagementCaseModel = CaseManagementCaseModel.objects.get(pk="d73fdf5a-9d37-11f0-87e1-00155dba6df9")
        # print(
        #     get_concat_address_from_case_instance(
        #     case_instance=case_instance
        #     )
        # )
        for query in CaseManagementCaseModel.objects.all():
            print("query", query)
            print(
                "get_sub_area_address_from_case_instance",
                save_sub_area_to_allocation_case_instance(case_instance=query),
            )
