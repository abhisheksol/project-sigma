from typing import List, Any
from django.contrib.auth.models import AbstractUser
from django.db import transaction, IntegrityError
from django.db.models.query import QuerySet
import logging

from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableFieldsModel,
    UserConfigTableOrderModel,
)

logger = logging.getLogger(__name__)


def get_or_create_user_table_order_instance(
    table_order_queryset: QuerySet[UserConfigTableOrderModel],
    feature_instance: CoreUtilsFeaturesModel,
    user_instance: AbstractUser,
    pagination_count: int,
) -> UserConfigTableOrderModel:
    """
    Get or create a UserConfigTableOrderModel instance for a given user and feature.
    Updates pagination size if already exists.
    """
    logger.debug(
        f"Getting/creating table order for user: {user_instance.username}, feature: {feature_instance.title}"
    )

    table_order_instance, created = UserConfigTableOrderModel.objects.get_or_create(
        user=user_instance,
        feature=feature_instance,
        defaults={"pagination_size": pagination_count},
    )

    if not created:
        # Update existing instance
        logger.debug(
            f"Updating existing table order instance: {table_order_instance.id}"
        )
        if table_order_instance.is_default:
            table_order_instance.is_default = False
        table_order_instance.pagination_size = pagination_count
        table_order_instance.save(update_fields=["is_default", "pagination_size"])

    logger.debug(f"Table order instance: {table_order_instance.id}, created: {created}")
    return table_order_instance


def create_or_update_table_fields(
    table_order_instance: UserConfigTableOrderModel,
    title: str,
    is_active: bool,
    order: int,
) -> UserConfigTableFieldsModel:
    """
    Create or update a UserConfigTableFieldsModel instance for a given table and field title.
    """
    logger.debug(
        f"Updating/creating field: {title}, is_active: {is_active}, order: {order}"
    )
    try:
        obj, created = UserConfigTableFieldsModel.objects.update_or_create(
            table=table_order_instance,
            title=title,
            defaults={"is_active": is_active, "order": order},
        )
        logger.debug(f"Field {title} {'created' if created else 'updated'}")
        return obj
    except IntegrityError as e:
        logger.error(f"IntegrityError for field {title}: {str(e)}")
        raise


def create_or_update_table_column_fields(
    feature_instance: CoreUtilsFeaturesModel,
    active_title: List[str],
    in_active_title: List[str],
    user_instance: AbstractUser,
    pagination_count: int = 10,
) -> UserConfigTableOrderModel:
    """
    Create or update column preferences for a given user and feature.
    Ensures fields update correctly, new ones are created, and old ones are removed.
    """
    logger.debug(
        f"Input - Active: {active_title}, Inactive: {in_active_title}, Pagination: {pagination_count}"
    )

    try:
        with transaction.atomic():
            # Get or create the table order instance
            table_order_instance: UserConfigTableOrderModel = (
                get_or_create_user_table_order_instance(
                    table_order_queryset=UserConfigTableOrderModel.objects.filter(
                        user=user_instance
                    ),
                    feature_instance=feature_instance,
                    user_instance=user_instance,
                    pagination_count=pagination_count,
                )
            )

            # Update active fields (order starts from 1)
            for idx, title in enumerate(active_title):
                create_or_update_table_fields(
                    table_order_instance=table_order_instance,
                    title=title,
                    is_active=True,
                    order=idx + 1,
                )

            # Update inactive fields (order continues after active fields)
            for idx, title in enumerate(in_active_title):
                create_or_update_table_fields(
                    table_order_instance=table_order_instance,
                    title=title,
                    is_active=False,
                    order=idx + len(active_title) + 1,
                )

            # Cleanup: remove fields not in payload
            current_titles: set = set(active_title + in_active_title)
            obsolete_fields: QuerySet[UserConfigTableFieldsModel] = (
                UserConfigTableFieldsModel.objects.filter(
                    table=table_order_instance
                ).exclude(title__in=current_titles)
            )
            logger.debug(f"Fields to delete: {list(obsolete_fields.values('title'))}")
            obsolete_fields.delete()

        # Verify final state
        final_state: List[Any] = UserConfigTableFieldsModel.objects.filter(
            table=table_order_instance
        ).values("title", "is_active", "order")
        logger.debug(f"Final state: {list(final_state)}")

        return table_order_instance

    except Exception as e:
        logger.error(f"Transaction failed: {str(e)}")
        raise
