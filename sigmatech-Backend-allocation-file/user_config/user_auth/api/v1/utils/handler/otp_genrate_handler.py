
from django.db import transaction
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
import random
from user_config.user_auth.models import UserModel
from user_config.user_auth.utils.email_templates.forgot_password_email_templates import (
    send_otp_email)


class OtpGenerateHandler(CoreGenericBaseHandler):

    def validate(self):
        print("otp generate handler=>", self.data.get('user'))
        # generate otp logic here random number

        if self.data.get('phone_number') is None:
            return self.set_error_message(error_message="phone number is required", key="phone_number")

        try:
            self.user_instance: UserModel = UserModel.objects.get(
                phone_number=self.data.get('phone_number'))
        except UserModel.DoesNotExist:
            return self.set_error_message(error_message="user not found", key="user")

    def create(self):
        with transaction.atomic():
            otp = random.randint(1000, 9999)

            self.data["otp"] = otp

            self.instance = self.queryset.create(
                user=self.user_instance,
                mobile_otp=otp
            )

            send_otp_email(
                user_instance=self.user_instance, otp=otp)

            print("otp instance=>", self.instance.mobile_otp)

            self.logger.info(
                f"OTP created successfully for user {self.instance.mobile_otp}")
