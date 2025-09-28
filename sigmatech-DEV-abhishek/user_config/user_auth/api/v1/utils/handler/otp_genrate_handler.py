
from django.db import transaction
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
import random
from user_config.user_auth.models import UserModel

class OtpGenerateHandler(CoreGenericBaseHandler):

    user_instance : UserModel= None

    def validate(self):
        print("otp generate handler=>",self.data.get('user'))
        # generate otp logic here random number

        self.user_instance : UserModel= UserModel.objects.get(id=self.data.get('user'))
        

        if self.user_instance is None:
            return self.set_error_message(error_message="user not found", key="user")
        


        
    
    def create(self):
        with transaction.atomic():
            otp= random.randint(1000,9999)
            
            
            self.instance= self.queryset.create(
                user= self.user_instance,
                mobile_otp= otp
            )
            print("otp instance=>",self.instance.mobile_otp)
            self.set_toast_message_value(f"OTP created successfully {self.instance.mobile_otp} ")
            self.get_toast_message_value(instance=self.instance)
            

            self.logger.info(f"OTP created successfully for user {self.instance.mobile_otp}")
            
            

        