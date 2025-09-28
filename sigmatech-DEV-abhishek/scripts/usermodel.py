from user_config.user_auth.models import UserModel, UserRoleModel
from user_config.accounts.models import UserDetailModel
from store.configurations.region_config.models import RegionConfigurationRegionModel

def run():
    # 1️⃣ Get the role
    role = UserModel.objects.get(phone_number="9876543211")  # or any role you want
    print("Role fetched:", role)

    # 2️⃣ Create a new user
    # user = UserModel.objects.create(
    #     login_id="newlogin123",
    #     username="New User",
    #     email="newuser@example.com",
    #     user_role=role,
    #     password="securepassword123",  # will be hashed automatically if you use set_password()
    #     phone_number="9876543211",
    #     is_superuser=False,
    #     is_staff=True
    # )

    # # Hash password properly
    # user.set_password("securepassword123")
    # user.save()

    # # 3️⃣ Create UserDetailModel for this new user
    # region_instance = RegionConfigurationRegionModel.objects.get(
    #     id="6851979e-96c2-11f0-8953-b48c9d5559d8"
    # )

    # detail = UserDetailModel.objects.create(
    #     user=user,
    #     blood_group="A+",
    #     vehicle_number="1234",
    #     emergency_phone_number="9876543210",
    #     emergency_contact_relation_name="Brother",
    #     emergency_contact_relation="Brother"
    # )

    # # If assigned_region is ManyToManyField
    # detail.assigned_region.set([region_instance])
    # detail.save()

    # print("User and detail created:", user, detail)
