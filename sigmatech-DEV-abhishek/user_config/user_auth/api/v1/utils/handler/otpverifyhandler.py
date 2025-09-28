
import jwt
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from user_config.user_auth.models import BlackListTokenModel, MobileOTPModel, UserModel
from django.db import transaction
from  core_utils.utils.jwt_token_utils import encode_jwt

from user_config.user_auth.api.v1.utils.authentication.user_login_utils import ValidateUserLogin
from user_config.user_auth.api.v1.utils.authentication.jwt_response_payload_handler_utils import jwt_response_payload_handler

class OtpverifyHandler(CoreGenericBaseHandler):
    def validate(self):
        user = self.data.get("user")
        mobile_otp = self.data.get("mobile_otp")

        self.user_instance = UserModel.objects.get(id=user)
        otp = MobileOTPModel.objects.filter(user=user, mobile_otp=mobile_otp, is_expired=False).first()

        if otp is None:
            self.set_error_message(error_message="Invalid OTP", key="mobile_otp")

    def create(self):
        with transaction.atomic():
            validate_user_login = ValidateUserLogin(
                login_id=self.user_instance.login_id,
                password="",  
                re_login=True
            )
            validate_user_login.user_instance = self.user_instance
            jwt_token = validate_user_login.set_jwt_token()  

            
            BlackListTokenModel.objects.create(user=self.user_instance, token=jwt_token, is_login=True)

            self.set_toast_message_value(f"OTP verified successfully {jwt_token}")
            self.get_toast_message_value(instance=self.user_instance)
            self.logger.info(f"OTP verified successfully for user {self.user_instance.pk}")
            print("JWT Token:", jwt_token)

            
            

        