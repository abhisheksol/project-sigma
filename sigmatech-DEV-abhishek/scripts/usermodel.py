from user_config.user_auth.models import UserModel
from store.operations.case_management.models import (
    CaseManagementCaseModel,
)

from user_config.accounts.models import (
    UserDetailModel,
)
# def run():

# get all pincode from the case,management
# customer_office_pin_code
pincodes= CaseManagementCaseModel.objects.all()

pincodes[0].customer_office_pin_code


a=pincodes[0].customer_office_pin_code


# ***********************************************

# Q2)fetch all user per pincode working 




user = UserModel.objects.filter(
    UserDetailModel_user__assigned_pincode__pincode__pincode=a.pincode.pincode
)



user

# Q3) get assigned case for that pincode 

case= CaseManagementCaseModel.objects.filter(
    customer_office_pin_code_pincode_pincode= 413006
)
case.count()