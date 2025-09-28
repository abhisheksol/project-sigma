
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from user_config.user_auth.models import BlackListTokenModel, MobileOTPModel, UserModel
from django.db import transaction
from  core_utils.utils.jwt_token_utils import encode_jwt

class OtpverifyHandler(CoreGenericBaseHandler):
    def validate(self):
        print("otp verify handler=---------->",self.data.get("mobile_otp"))
        
        user= self.data.get('user')
        mobile_otp= self.data.get('mobile_otp')

        self.user_instance= UserModel.objects.get(id=user)

        
        otp= MobileOTPModel.objects.filter(
            user= user,
            mobile_otp= mobile_otp,
            is_expired= False
        ).first()

        if otp is None:
            self.set_error_message(error_message="Invalid OTP", key="mobile_otp")

    def create(self):
        with transaction.atomic():
            print("=========>",self.user_instance.pk)

            
            token = encode_jwt(user_id=str(self.user_instance.pk))
            print("token===>",token)
            res=BlackListTokenModel.objects.create(user=self.user_instance, token=token, is_login=True)
            print("res===>",res.token)

            self.set_toast_message_value(f" OTP verified successfully ")

            self.logger.info(f" OTP verified successfully for user {self.user_instance.pk}")


        