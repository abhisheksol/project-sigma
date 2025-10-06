
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from user_config.user_auth.models import BlackListTokenModel, MobileOTPModel, UserModel
from django.db import transaction

from user_config.user_auth.api.v1.utils.authentication.user_login_utils import ValidateUserLogin


class OtpverifyHandler(CoreGenericBaseHandler):
    def validate(self):
        phone_number: str = self.data.get("phone_number")
        mobile_otp: str = self.data.get("mobile_otp")

        try:
            self.user_instance: UserModel = UserModel.objects.get(
                phone_number=phone_number)
        except UserModel.DoesNotExist:
            return self.set_error_message(error_message="user not found", key="user")

        print("user instance in otp verify handler=>",
              self.user_instance.login_id)
        otp = MobileOTPModel.objects.filter(
            user=self.user_instance, mobile_otp=mobile_otp, is_expired=False).first()

        if otp is None:
            self.set_error_message(
                error_message="Invalid OTP", key="mobile_otp")

    def create(self):
        with transaction.atomic():
            validate_user_login = ValidateUserLogin(
                login_id=self.user_instance.login_id,
                password="",
                re_login=True
            )
            validate_user_login.user_instance = self.user_instance
            jwt_token = validate_user_login.set_jwt_token()

            self.data["jwt_token"] = jwt_token

            BlackListTokenModel.objects.create(
                user=self.user_instance, token=jwt_token, is_login=True)

            # self.set_toast_message_value(
            #     f"OTP verified successfully {jwt_token}")
            # self.get_toast_message_value(instance=self.user_instance)
            self.logger.info(
                f"OTP verified successfully for user {self.user_instance.pk}")
