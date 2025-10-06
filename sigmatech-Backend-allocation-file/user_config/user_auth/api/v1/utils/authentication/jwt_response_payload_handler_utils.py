import logging
from datetime import datetime
from typing import List
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils.timezone import now as django_now
from rest_framework.request import Request

from core.settings import logger
from core_utils.activity_monitoring.enums import ActivityMonitoringMethodTypeEnumChoices
from core_utils.activity_monitoring.models import ActivityMonitoringLogModel
from core_utils.utils.db_utils.activity_monitoring import activity_monitoring_logger
from user_config.user_auth.models import BlackListTokenModel, LoginAnalyticsModel

# ? ? Configuring logger with the app name "JWTSettings"
logger = logging.LoggerAdapter(logger, {"app_name": "JWTSettings"})
#
DISABLE_MULTI_LOGIN: List = getattr(settings, "DISABLE_MULTI_LOGIN", True)


class UserLoginCreateUtils:
    """
    Utility class for handling user login, analytics, and token management.
    This class helps track user login activity, store analytics, and handle JWT token blacklisting.

    Attributes:
        request (Request): The Django Rest Framework request object.
        meta (dict): Metadata from the request object.
        user_agent (str | None): The user agent string from the request headers.
        user_instance (AbstractBaseUser): The authenticated user instance.
        token (str | None): The JWT token assigned to the user session.
    """

    request: Request
    meta: dict
    user_agent: str | None
    user_instance: AbstractBaseUser
    token: str | None

    def __init__(
        self, request: Request, user_instance: AbstractBaseUser, token: str = None
    ):
        """
        Initializes the UserLoginCreateUtils instance.

        Args:
            request (Request): The API request object.
            user_instance (AbstractBaseUser): The authenticated user instance.
            token (str, optional): The JWT token assigned to the session. Defaults to None.
        """
        self.request: Request = request
        self.meta: dict = request.META
        self.user_agent: str = request.META.get("HTTP_USER_AGENT")
        self.user_instance: AbstractBaseUser = user_instance
        self.token: str = token

    def get_ip_address(self) -> str:
        """
        Retrieves the IP address of the client making the request.

        Returns:
            str: The extracted IP address.
        """
        x_forwarded_for: str | None = self.meta.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # ? Extract first IP in case of multiple proxies
            ip: str = x_forwarded_for.split(",")[0]
        else:
            # ? Default IP if not found
            ip: str = self.meta.get("REMOTE_ADDR", "0.0.0.0")
        return ip

    def add_user_login_analytics_instance(self, token: str) -> LoginAnalyticsModel:
        """
        Creates a login analytics record for the user.

        Args:
            token (str): The JWT token used for login.

        Returns:
            LoginAnalyticsModel: The created login analytics instance.
        """
        user_login_analytics_queryset: QuerySet[LoginAnalyticsModel] = (
            LoginAnalyticsModel.objects.filter(user=self.user_instance)
        )

        logger.info(f"User Agent: {self.user_agent}")
        logger.info(f"User IP Address: {self.get_ip_address()}")

        login_analytics_instance = user_login_analytics_queryset.create(
            user=self.user_instance,
            ip_address=self.get_ip_address(),
            login_count=user_login_analytics_queryset.count() + 1,
            device_name=self.user_agent,
            token=token,
        )

        logger.info(f"Login Analytics Instance Created: {login_analytics_instance}")
        return login_analytics_instance

    def create_and_block_existing_token(self, token: str) -> BlackListTokenModel:
        """
        Blacklists any existing tokens and creates a new token entry.

        Args:
            token (str): The new JWT token to be assigned.

        Returns:
            BlackListTokenModel: The latest created blacklist token instance.
        """
        with transaction.atomic():
            blacklist_token_queryset: QuerySet[BlackListTokenModel] = (
                BlackListTokenModel.objects.filter(
                    user=self.user_instance, is_login=True, is_delete=False
                )
            )

            active_blacklist_token_instances: QuerySet[BlackListTokenModel] = (
                blacklist_token_queryset.filter(is_login=True)
            )

            # ? If re-login is requested, deactivate existing tokens
            if self.request.data.get("re_login", False):
                if not DISABLE_MULTI_LOGIN:
                    tokens_updated: int = active_blacklist_token_instances.update(
                        is_login=False, is_delete=True
                    )
                    logger.info(f"Tokens Deactivated: {tokens_updated}")

            # ? Create new blacklist token entry
            latest_blacklist_token: BlackListTokenModel = (
                blacklist_token_queryset.create(
                    user=self.user_instance, is_login=True, token=token
                )
            )
            # ? log activity
            activity_log_instance: ActivityMonitoringLogModel = (
                activity_monitoring_logger(
                    instance=latest_blacklist_token,
                    user=self.user_instance,
                    method=ActivityMonitoringMethodTypeEnumChoices.CREATE.value,
                    activity_type="LOGIN_ACTIVITY_LOG",
                    new_instance=latest_blacklist_token,
                )
            )

            activity_log_instance.description = (
                f"{self.user_instance.username} logged in successfully"
            )
            activity_log_instance.save()
            logger.info(f"New Blacklist Token Created: {latest_blacklist_token}")

            # ? Record user login analytics
            self.add_user_login_analytics_instance(token=token)

        return latest_blacklist_token

    def update_user_instance(self) -> None:
        """
        Updates the last login timestamp for the user.
        """
        self.user_instance.last_login = django_now()
        self.user_instance.save()

    def get_jwt_response_payload(self) -> dict:
        """
        Constructs the JWT response payload.

        Returns:
            dict: The response payload containing user and token details.
        """
        return {
            "token": self.token,
            "user_id": self.user_instance.pk,
            "email": self.user_instance.email,
            "is_active": self.user_instance.is_active,
            "is_verified": self.user_instance.is_verified,
            "is_approved": self.user_instance.is_approved,
            "ip_address": self.get_ip_address(),
            "user_role_id": str(self.user_instance.user_role.pk),
            "user_role": self.user_instance.user_role.role,
            "reports_to": (
                str(self.user_instance.reports_to.pk)
                if self.user_instance.reports_to
                else None
            ),
            "reports_to_username": (
                self.user_instance.reports_to.username
                if self.user_instance.reports_to
                else None
            ),
            "profile_picture": self.user_instance.UserDetailModel_user.profile_picture,
            "username": self.user_instance.username,
        }


def jwt_response_payload_handler(
    token: str, user: AbstractBaseUser, request: Request, issued_at: datetime = None
) -> dict:
    """
    Custom response payload handler for Django Rest Framework JWT.

    This function processes user login, blacklists old tokens, updates login timestamps,
    and returns a structured response.

    Args:
        token (str): The JWT token issued.
        user (AbstractBaseUser): The authenticated user instance.
        request (Request): The API request object.
        issued_at (datetime, optional): The timestamp when the token was issued.

    Returns:
        dict: The JWT response payload.
    """
    login_utils = UserLoginCreateUtils(request=request, user_instance=user, token=token)

    # ? Blacklist old tokens and create a new one
    login_utils.create_and_block_existing_token(token=token)

    # ? Update last login timestamp
    login_utils.update_user_instance()

    logger.info(f"Token Issued At: {issued_at}")
    logger.info(f"{str(user)} Logged in sucessfully")
    # ? Return structured response payload
    return login_utils.get_jwt_response_payload()
