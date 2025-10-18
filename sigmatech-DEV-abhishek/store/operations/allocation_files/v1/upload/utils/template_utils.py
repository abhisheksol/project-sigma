from typing import List
from django.db.models.query import QuerySet
from store.configurations.loan_config.models import (
    LoanConfigurationsProductAssignmentModel,
)
from store.configurations.loan_config.template_config.models import (
    ProcessTemplateFieldMappingModel,
    ProcessTemplatePreferenceModel,
)
from core.settings import logger
import logging

# Initialize logger with application name context
logger: logging.LoggerAdapter = logging.LoggerAdapter(logger, {"app_name": __name__})


def get_default_process_product_assigned_template_instance(
    product_assignment_instance: LoanConfigurationsProductAssignmentModel,
) -> ProcessTemplatePreferenceModel:
    """
    Retrieves the default ProcessTemplatePreferenceModel instance associated with the given product assignment.

    Args:
        product_assignment_instance (LoanConfigurationsProductAssignmentModel): The product assignment instance to query.

    Returns:
        ProcessTemplatePreferenceModel: The default template instance.

    Raises:
        ProcessTemplatePreferenceModel.DoesNotExist: If no default template is found for the product assignment.
    """
    logger.info(
        f"Fetching default template for product assignment: {product_assignment_instance.id}"
    )
    instance: ProcessTemplatePreferenceModel = (
        ProcessTemplatePreferenceModel.objects.get(
            product_assignment=product_assignment_instance, is_default=True
        )
    )
    logger.info(f"Retrieved default template instance: {instance.id}")
    return instance


def get_template_field_queryset(
    product_assignment_instance: LoanConfigurationsProductAssignmentModel,
) -> QuerySet[ProcessTemplateFieldMappingModel]:
    """
    Retrieves all ProcessTemplateFieldMappingModel instances associated with the default template
    for the given product assignment.

    Args:
        product_assignment_instance (LoanConfigurationsProductAssignmentModel): The product assignment instance to query.

    Returns:
        QuerySet[ProcessTemplateFieldMappingModel]: Queryset of template field mappings.

    Raises:
        ProcessTemplatePreferenceModel.DoesNotExist: If no default template is found.
    """
    logger.info(
        f"Fetching template field queryset for product assignment: {product_assignment_instance.id}"
    )
    # Get the default template instance
    instance: ProcessTemplatePreferenceModel = (
        get_default_process_product_assigned_template_instance(
            product_assignment_instance=product_assignment_instance
        )
    )
    logger.info(f"Using template instance: {instance.id}")
    # Query all field mappings for the template
    queryset: QuerySet[ProcessTemplateFieldMappingModel] = (
        ProcessTemplateFieldMappingModel.objects.filter(template=instance)
    )
    logger.info(f"Retrieved {queryset.count()} template field mappings")
    return queryset


def get_required_template_field_queryset(
    product_assignment_instance: LoanConfigurationsProductAssignmentModel,
) -> QuerySet[ProcessTemplateFieldMappingModel]:
    """
    Retrieves required ProcessTemplateFieldMappingModel instances associated with the default template
    for the given product assignment.

    Args:
        product_assignment_instance (LoanConfigurationsProductAssignmentModel): The product assignment instance to query.

    Returns:
        QuerySet[ProcessTemplateFieldMappingModel]: Queryset of required template field mappings.

    Raises:
        ProcessTemplatePreferenceModel.DoesNotExist: If no default template is found.
    """
    logger.info(
        f"Fetching required template field queryset for product assignment: {product_assignment_instance.id}"
    )
    # Get the default template instance
    instance: ProcessTemplatePreferenceModel = (
        get_default_process_product_assigned_template_instance(
            product_assignment_instance=product_assignment_instance
        )
    )
    logger.info(f"Using template instance: {instance.id}")
    # Query required field mappings for the template
    queryset: QuerySet[ProcessTemplateFieldMappingModel] = (
        ProcessTemplateFieldMappingModel.objects.filter(
            template=instance, is_required_field=True
        )
    )
    logger.info(f"Retrieved {queryset.count()} required template field mappings")
    return queryset


def get_template_fields_list(
    product_assignment_instance: LoanConfigurationsProductAssignmentModel,
    field: str = "title",
) -> List[str]:
    """
    Retrieves a list of field values (default: titles) from the template field mappings
    associated with the default template for the given product assignment.

    Args:
        product_assignment_instance (LoanConfigurationsProductAssignmentModel): The product assignment instance to query.
        field (str, optional): The field to extract from the queryset. Defaults to "title".

    Returns:
        List[str]: List of field values from the template field mappings.

    Raises:
        ProcessTemplatePreferenceModel.DoesNotExist: If no default template is found.
    """
    logger.info(
        f"Fetching template fields list (field: {field}) for product assignment: {product_assignment_instance.id}"
    )
    # Get the template field queryset
    queryset: QuerySet[ProcessTemplateFieldMappingModel] = get_template_field_queryset(
        product_assignment_instance=product_assignment_instance
    )
    # Extract the specified field values as a list
    field_list: List[str] = list(queryset.values_list(field, flat=True))
    logger.info(f"Retrieved {len(field_list)} template field values")
    return field_list


def get_template_required_fields_list(
    product_assignment_instance: LoanConfigurationsProductAssignmentModel,
    field: str = "title",
) -> List[str]:
    """
    Retrieves a list of field values (default: titles) from the required template field mappings
    associated with the default template for the given product assignment.

    Args:
        product_assignment_instance (LoanConfigurationsProductAssignmentModel): The product assignment instance to query.
        field (str, optional): The field to extract from the queryset. Defaults to "title".

    Returns:
        List[str]: List of required field values from the template field mappings.

    Raises:
        ProcessTemplatePreferenceModel.DoesNotExist: If no default template is found.
    """
    logger.info(
        f"Fetching required template fields list (field: {field}) for product assignment: {product_assignment_instance.id}"
    )
    # Get the required template field queryset
    queryset: QuerySet[ProcessTemplateFieldMappingModel] = (
        get_required_template_field_queryset(
            product_assignment_instance=product_assignment_instance
        )
    )
    # Extract the specified field values as a list
    field_list: List[str] = list(queryset.values_list(field, flat=True))
    logger.info(f"Retrieved {len(field_list)} required template field values")
    return field_list
