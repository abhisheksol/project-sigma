from core.settings import PROJECT_NAME, PROJECT_LOGO, PROJECT_COMPANY_URL
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from core.settings import FRONTEND_URL, PROJECT_NAME, PROJECT_LOGO, PROJECT_COMPANY_URL
from core_utils.utils.smtp import send_an_email
from django.template import EngineHandler


def forgot_password_send_email(
    user_instance: get_user_model,
    token: str,
) -> None:

    # Create the email content
    context: dict = {
        "username": user_instance.username,
        "reset_link": f"{FRONTEND_URL}auth/reset-password?token={token}",
        "token": token,
        "PROJECT_LOGO": PROJECT_LOGO,
        "PROJECT_COMPANY_URL": PROJECT_COMPANY_URL,
    }
    print("context------------>", context)

    message: EngineHandler = render_to_string("auth/resetPassword.html", context)
    print("message", message)
    send_an_email(
        **{
            "receiver_email": user_instance.email,
            "subject": f"{PROJECT_NAME} | Forgot password",
            "body": message,
        }
    )


# user_config/user_auth/utils/email_templates/otp_email_templates.py


def send_otp_email(user_instance: get_user_model, otp: str) -> None:

    context: dict = {
        "username": user_instance.username,
        "otp": otp,
        "PROJECT_LOGO": PROJECT_LOGO,
        "PROJECT_COMPANY_URL": PROJECT_COMPANY_URL,
    }
    print("OTP email context------------>", context)

    # Render the email template
    message: EngineHandler = render_to_string("auth/sendOtp.html", context)
    print("OTP email message------------>", message)

    # Send the email
    send_an_email(
        **{
            "receiver_email": user_instance.email,
            "subject": f"{PROJECT_NAME} ",
            "body": message,
        }
    )
