import json
import logging
from core.settings import logger
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from typing import Union


class NotificationConsumer(WebsocketConsumer):
    """
    WebSocket consumer for Notifications
    """

    logger: logging.LoggerAdapter = logging.LoggerAdapter(
        logger, {"app_name": "NotificationConsumer"}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_instance: Union[str, None] = None
        self.user_custom_id: Union[str, None] = None
        self.conversation_name: Union[str, None] = None

    def connect(self):
        try:
            self.logger.info("WebSocket Connection Initialized")
            self.accept()

            # Set a simple static group name for testing
            self.conversation_name = "test_notifications"

            # Log test user info (not a real user for now)
            self.user_instance = "test_user"
            self.user_custom_id = "test_id"

            # Join group
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )

            self.logger.info(
                f"WebSocket test connection established for {self.user_instance}"
            )

            # Send initial test message
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "notification_status",
                    "conversations": self.conversation_name,
                    "data": {
                        "has_notifications": True,
                        "message": "Test connection successful",
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Error while connecting to websocket: {str(e)}")
            self.close(code=4000, reason=f"Connection Error: {str(e)}")

    def disconnect(self, close_code):
        try:
            self.logger.info(
                f"User {self.user_custom_id} got disconnected from {self.conversation_name}"
            )
            self.mark_as_offline()
            async_to_sync(self.channel_layer.group_discard)(
                self.conversation_name, self.channel_name
            )
        except Exception as e:
            self.logger.error(
                f"Error during disconnect in Notification Layer: {str(e)}"
            )

    def pop_up_notification(self, event):
        # ? Send the new activity data to WebSocket
        self.send(text_data=json.dumps(event))

    def notification_status(self, event):
        # ? Send the new activity data to WebSocket
        self.send(text_data=json.dumps(event))
