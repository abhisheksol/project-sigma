from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from core.settings import FRONTEND_URL, PROJECT_NAME, PROJECT_LOGO, PROJECT_COMPANY_URL
from core_utils.utils.smtp import send_an_email
from django.template import EngineHandler


def forgot_password_send_email(
    user_instance: get_user_model,
    token: str,
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
        "reset_link": f"{FRONTEND_URL}auth/reset-password?token={token}",
        "token": token,
        "PROJECT_LOGO": PROJECT_LOGO,
        "PROJECT_COMPANY_URL": PROJECT_COMPANY_URL,
    }
    print("context", context)

    message: EngineHandler = render_to_string("auth/resetPassword.html", context)
    print("message", message)
    send_an_email(
        **{
            "receiver_email": user_instance.email,
            "subject": f"{PROJECT_NAME} | Forgot password",
            "body": message,
        }
    )
