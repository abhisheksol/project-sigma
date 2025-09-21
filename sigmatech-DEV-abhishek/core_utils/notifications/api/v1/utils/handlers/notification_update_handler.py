from django.db import transaction
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db.models import QuerySet
from django.utils.timezone import now as django_now


class CoreUtilsNotificationModelUpdateHandler(CoreGenericBaseHandler):
    """
    Handles the updating of notifications
    """

    def validate(self):
        notification_queryset: QuerySet = self.queryset.filter(
            user=self.request.user,
            company=self.get_company_instance(),
        )
        if not self.data["mark_all_as_read"]:
            if (
                "mark_as_read" in self.data
                and self.data["mark_as_read"]
                and notification_queryset.filter(
                    pk__in=self.data["mark_as_read"]
                ).count()
                < len(self.data["mark_as_read"])
            ):
                return self.set_error_message(
                    error_message={
                        "title": "Failed to Mark as Read",
                        "description": "One or more notification ids are invalid.",
                    }
                )
        if not self.data["mark_all_as_cleared"]:
            if (
                "mark_as_cleared" in self.data
                and self.data["mark_as_cleared"]
                and notification_queryset.filter(
                    pk__in=self.data["mark_as_cleared"]
                ).count()
                < len(self.data["mark_as_cleared"])
            ):
                return self.set_error_message(
                    error_message={
                        "title": "Failed to Clear Notification",
                        "description": "One or more notification ids are invalid.",
                    }
                )

    def create(self):
        try:
            with transaction.atomic():
                notification_queryset: QuerySet = self.queryset.filter(
                    user=self.request.user,
                    company=self.get_company_instance(),
                )
                if self.data["mark_all_as_read"]:
                    notification_queryset.filter(is_read=False).filter(
                        **self.get_filters()
                    ).update(is_read=True, read_at=django_now())
                elif "mark_as_read" in self.data and self.data["mark_as_read"]:
                    notification_queryset.filter(
                        pk__in=self.data["mark_as_read"], is_read=False
                    ).update(is_read=True, read_at=django_now())
                if self.data["mark_all_as_cleared"]:
                    notification_queryset.filter(is_cleared=False).filter(
                        **self.get_filters()
                    ).update(is_cleared=True, cleared_at=django_now())
                elif "mark_as_cleared" in self.data and self.data["mark_as_cleared"]:
                    notification_queryset.filter(
                        pk__in=self.data["mark_as_cleared"], is_cleared=False
                    ).update(is_cleared=True, cleared_at=django_now())
        except Exception as e:
            raise Exception(f"Error while updating notifications : {str(e)}")

    def get_filters(self) -> dict:
        """
        Based on the tab index adds the filter
        """
        tab_index: int = self.data["tab"]
        filters: dict = {}
        if self.request.user.UserDetailModel_user.role.pk == 1:
            if tab_index == 1:
                filters["is_mention"] = False
                filters["is_cleared"] = False
            elif tab_index == 2:
                filters["is_cleared"] = True
        else:
            if tab_index == 1:
                filters["is_cleared"] = False
            elif tab_index == 2:
                filters["is_mention"] = True
            elif tab_index == 3:
                filters["is_mention"] = False
            elif tab_index == 4:
                filters["is_cleared"] = True
        return filters
