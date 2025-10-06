from django.template.loader import render_to_string
from core.settings import FRONTEND_URL, PROJECT_NAME, PROJECT_LOGO
from core_utils.utils.smtp import send_an_email
from django.template import EngineHandler
from user_config.user_auth.models import UserModel


def user_create_send_email(
    user_instance: UserModel,
    password: str,
) -> None:
    """
    Sends a forgot password email to the user with a link to reset their password.

    Args:
        email (str): The email address of the user.
        ui_host (str): The host URL for the UI where the password reset page is located.

    Returns:
        None
    """

    # Create the email content
    context: dict = {
        "username": user_instance.username,
        "email": user_instance.email,
        "reset_link": FRONTEND_URL,
        "password": password,
        "PROJECT_LOGO": PROJECT_LOGO,
    }

    message: EngineHandler = render_to_string("auth/new_user.html", context)
    send_an_email(
        **{
            "receiver_email": user_instance.email,
            "subject": f"{PROJECT_NAME} | Your Account is Ready 🎉",
            "body": message,
        }
    )
