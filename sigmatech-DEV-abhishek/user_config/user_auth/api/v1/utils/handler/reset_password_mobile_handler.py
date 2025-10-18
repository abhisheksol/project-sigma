# from core_utils.utils.jwt_token_utils import encode_jwt
# from user_config.user_auth.models import OTPModel


# class UserAuthUserResetPasswordMobileHandler(CoreGenericBaseHandler):
#     """
#     Handles reset password via mobile OTP.
#     """

#     user_instance = None
#     otp_instance = None

#     def validate(self) -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
#         otp = self.data.get("otp")
#         password = self.data.get("password")

#         if not otp:
#             return self.set_error_message("OTP is required.")
#         if not password:
#             return self.set_error_message("Password is required.")

#         try:
#             self.otp_instance = OTPModel.objects.get(otp=otp, is_used=False)
#         except OTPModel.DoesNotExist:
#             return self.set_error_message("Invalid OTP.")

#         if self.otp_instance.is_expired():
#             return self.set_error_message("OTP expired.")

#         self.user_instance = self.otp_instance.user

#     def create(self) -> Dict[str, str]:
#         self.user_instance.set_password(self.data.get("password"))
#         self.user_instance.save()

#         self.otp_instance.is_used = True
#         self.otp_instance.save()

#         access_token = encode_jwt(user_id=str(self.user_instance.pk))
#         return {"message": "Password reset successfully.", "access_token": access_token}
