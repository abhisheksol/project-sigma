from django.urls import path
from core_utils.notifications.web_socket.consumer import NotificationConsumer
from typing import List

websocket_urlpatterns: List = [
    path("ws/notifications/<str:user_id>/", NotificationConsumer.as_asgi()),
]
