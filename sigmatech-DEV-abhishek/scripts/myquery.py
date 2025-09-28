from store.configurations.region_config.models import (
    RegionConfigurationAreaModel,
    RegionConfigurationCityModel,
    RegionConfigurationPincodeModel,
    RegionConfigurationRegionModel,
    RegionConfigurationZoneModel,
)
from user_config.user_auth.models import (UserModel ,UserRoleModel,
                                          
                                          MobileOTPModel)


def run():
    user_instance= UserModel.objects.get(id="9ce6b435-9761-11f0-86fe-b48c9d5559d8")
    
    otp= MobileOTPModel.objects.create(
        user= user_instance,
        mobile_otp="222",
        is_expired= False
    )
    print(otp)
    print("otp created successfully")
    
