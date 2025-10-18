from django.utils import timezone
from datetime import timedelta
import random
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from user_config.user_auth.models import OTPModel, UserModel
from typing import Optional, Dict, Union


class UserAuthUserForgotPasswordMobileHandler(CoreGenericBaseHandler):

    def validate(self) -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
        login_id = self.data.get("login_id")

        try:
            self.user_instance: UserModel = UserModel.objects.get(
                email__iexact=login_id, is_active=True
            )
        except UserModel.DoesNotExist:
            return self.set_error_message("User not found.")

    def create(self) -> None:
        otp: str = str(random.randint(1000, 9999))
        expires_at: timezone.now = timezone.now() + timedelta(minutes=5)

        OTPModel.objects.update_or_create(
            user=self.user_instance,
            defaults={"otp": otp, "expires_at": expires_at, "is_used": False},
        )

        # Here you can integrate SMS sending
        print(f"Sending OTP {otp} to user {self.user_instance.email}")
        print(self.data)
        # return self.set_success_message("OTP sent successfully.")
