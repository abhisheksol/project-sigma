"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import django
import os
from core_utils.notifications.web_socket.routing import (
    websocket_urlpatterns as notification_websocket_urlpatterns,
)
from django.core.handlers.asgi import ASGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()


django_asgi_application: ASGIHandler = get_asgi_application()


application: ProtocolTypeRouter = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([*notification_websocket_urlpatterns]))
        ),
    }
)
