from core_utils.utils.enums import get_enum_value_with_key
from core_utils.utils.file_utils.extract import fetch_dataframe_from_url
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from django.db.models.query import QuerySet
from typing import Optional, List, Dict
from store.configurations.loan_config.template_config.enums import (
    CustomAllocationFileTemplateReservedFieldsEnum,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
    ProcessTemplatePreferenceModel,
)
from pandas.core.frame import DataFrame


class TemplateMappingConfigUtils:
    """
    Utility class to handle mapping of template files (Excel/CSV)
    to process and product assignment instances.

    Responsibilities:
        - Read Excel/CSV template files
        - Convert them into JSON-like mappings
        - Create or update ProcessTemplatePreferenceModel instances
        - Assign ProcessTemplateFieldMappingModel entries based on file data
    """

    __product_assignment_instance: LoanConfigurationsProductAssignmentModel
    __template_preference_instance: ProcessTemplatePreferenceModel
    __template_url: str
    __template_mapping_queryset: QuerySet[ProcessTemplateFieldMappingModel] = (
        ProcessTemplateFieldMappingModel.objects.all()
    )

    def __init__(
        self,
        product_assignment_instance: LoanConfigurationsProductAssignmentModel,
        template_url: str,
    ):
        """
        Initialize TemplateMappingConfigUtils.

        Args:
            product_assignment_instance (LoanConfigurationsProductAssignmentModel):
                The product assignment instance for which template is being configured.
            template_url (str):
                URL to the uploaded template file (Excel/CSV).
        """
        self.__product_assignment_instance: LoanConfigurationsProductAssignmentModel = (
            product_assignment_instance
        )
        self.__template_url: str = template_url

    def __excel_to_json(self) -> Dict[str, Dict[str, str]]:
        """
        Reads Excel/CSV file from URL and converts it into a dictionary.

        Returns:
            Dict[str, Dict[str, str]]:
                A nested dictionary where keys are product titles
                and values are mappings of field name → status (R, Y, etc.).
        """
        # Load DataFrame from given file URL
        df: DataFrame = fetch_dataframe_from_url(self.__template_url)

        # Convert DataFrame into nested dictionary by transposing
        transposed_dict: Dict[str, Dict[str, str]] = {
            product: {row["Field Name"]: row[product] for _, row in df.iterrows()}
            for product in df.columns
            if product != "Field Name"
        }
        return transposed_dict

    def __product_template_data(self) -> Dict[str, str]:
        """
        Extract template data specific to the assigned product.

        Returns:
            Dict[str, str]: Field name → status mapping for the product.
        """
        return self.__excel_to_json()[self.__product_assignment_instance.product.title]

    def __create_template_instance(self) -> ProcessTemplatePreferenceModel:
        """
        Creates or updates a ProcessTemplatePreferenceModel instance
        for the product assignment.

        Returns:
            ProcessTemplatePreferenceModel: Created or updated template instance.
        """
        self.__template_preference_instance, _ = (
            ProcessTemplatePreferenceModel.objects.update_or_create(
                title=f"{self.__product_assignment_instance.process.title}-{self.__product_assignment_instance.product.title} Template",
                product_assignment=self.__product_assignment_instance,
                uploaded_file=self.__template_url,
            )
        )
        return self.__template_preference_instance

    def __product_template_assignment(
        self, template_preference_instance: ProcessTemplatePreferenceModel
    ):
        """
        Assigns template fields to a given template instance by creating or updating
        ProcessTemplateFieldMappingModel entries.

        Args:
            template_preference_instance (ProcessTemplatePreferenceModel):
                The template preference instance.

        Returns:
            List[ProcessTemplateFieldMappingModel]: List of mapping instances created/updated.
        """
        template_data = self.__product_template_data()
        map_instance_list: List[ProcessTemplateFieldMappingModel] = []

        # Iterate over all field keys in the template data
        for key in template_data.keys():
            print(
                key,
                get_enum_value_with_key(
                    enum_class=CustomAllocationFileTemplateReservedFieldsEnum, key=key
                ),
            )

            # Determine if field is required or optional
            is_required_field: Optional[bool] = None
            if template_data[key] == "R":
                is_required_field: bool = True
            elif template_data[key] == "Y":
                is_required_field: bool = False

            # Create or update mapping if valid status is found
            if is_required_field is not None:
                map_instance: ProcessTemplateFieldMappingModel = (
                    self.__template_mapping_queryset.update_or_create(
                        template=template_preference_instance,
                        title=get_enum_value_with_key(
                            enum_class=CustomAllocationFileTemplateReservedFieldsEnum,
                            key=key,
                        ),
                        label=key,
                        is_required_field=is_required_field,
                    )
                )
                map_instance_list.append(map_instance)
            else:
                # Delete mapping if field is not marked as required/optional
                self.__template_mapping_queryset.filter(
                    template=template_preference_instance,
                    title=get_enum_value_with_key(
                        enum_class=CustomAllocationFileTemplateReservedFieldsEnum,
                        key=key,
                    ),
                ).delete()

        return map_instance_list

    def _assign_template_for_template_instace(
        self, template_preference_instance: ProcessTemplatePreferenceModel
    ):
        """
        Public method wrapper to assign template fields
        for a given template instance.

        Args:
            template_preference_instance (ProcessTemplatePreferenceModel):
                Template instance to assign fields to.

        Returns:
            List[ProcessTemplateFieldMappingModel]: Created/updated field mapping instances.
        """
        return self.__product_template_assignment(
            template_preference_instance=template_preference_instance
        )

    def _assign_template_for_product_assignment_instance(
        self, product_assignment_instance: LoanConfigurationsProductAssignmentModel
    ):
        """
        Assigns template for a given product assignment instance.

        Args:
            product_assignment_instance (LoanConfigurationsProductAssignmentModel):
                Product assignment instance to assign template for.
        """
        # Update internal reference to product assignment
        self.__product_assignment_instance: LoanConfigurationsProductAssignmentModel = (
            product_assignment_instance
        )

        # Create template preference instance
        self.__template_preference_instance: ProcessTemplatePreferenceModel = (
            self.__create_template_instance()
        )

        # Assign fields to created template instance
        self._assign_template_for_template_instace(
            template_preference_instance=self.__template_preference_instance
        )

    def assign_template_to_product_assignment(self):
        """
        Public entry point to assign a template to the
        stored product assignment instance.
        """
        self._assign_template_for_product_assignment_instance(
            self.__product_assignment_instance
        )
