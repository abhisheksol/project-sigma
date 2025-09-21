from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.settings import PROJECT_NAME, FRONTEND_URL
from user_config.accounts.models import UserDetailModel
from user_config.user_auth.enums import UserRoleEnum
from user_config.user_auth.models import UserRoleModel

from django.db import transaction
from uuid import uuid1
from typing import List, Dict, Any


class Command(BaseCommand):
    """
    Custom Django management command to load predefined users into the system,
    assign them roles, create UserDetailModel, and email their credentials.
    """

    def get_load_user_data(self) -> List[Dict[str, Any]]:
        """
        Returns a list of user data dictionaries to be loaded into the system.

        Returns:
            List[Dict[str, Any]]: Predefined user data including credentials and contact info.
        """
        return [
            {
                "username": "admin",
                "login_id": "admin",
                "email": "admin@admin.com",
                "password": "Abcd.1234",
                "phone_number": "9876543210",
            }
            # {
            #     "username": "koushik",
            #     "login_id": "koushik",
            #     "email": "koushik.kumar@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "8123296486",
            # },
            # {
            #     "username": "Vamsi Madugundu",
            #     "login_id": "vamsi",
            #     "email": "vamsi.madugundu@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "9441038593",
            # },
            # {
            #     "username": "Likhita Parcha",
            #     "login_id": "likhita",
            #     "email": "likhita.parcha@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "8008709849",
            # },
            # {
            #     "username": "Abhishek Mekala",
            #     "login_id": "abhishek",
            #     "email": "abhishek@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "8867874100",
            # },
            # {
            #     "username": "Abhishek Solapure",
            #     "login_id": "abhisheks",
            #     "email": "abhishek.solapure@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "9561435141",
            # },
            # {
            #     "username": "Krishn Yenamandra",
            #     "login_id": "krishnyenamandra",
            #     "email": "krishn@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "9177580929",
            # },
            # {
            #     "username": "Monica Waghray",
            #     "login_id": "Monica",
            #     "email": "monica.waghray@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "7304155063",
            # },
            # {
            #     "username": "rohith baggam",
            #     "login_id": "rohithbaggam",
            #     "email": "rohith.baggam@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "7093389378",
            # },
            # {
            #     "username": "ykrishn",
            #     "login_id": "ykrishn",
            #     "email": "ykrishn@gmail.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "9177580928",
            # },
            # {
            #     "username": "Harini Aduri",
            #     "login_id": "harini",
            #     "email": "harini.aduri@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "9885149081",
            # },
            # {
            #     "username": "Sairam Gaddam",
            #     "login_id": "sairam",
            #     "email": "sairam@aptagrim.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "6548782101",
            # },
            # {
            #     "username" : "supervsior user",
            #     "login_id" : "supervsioruser",
            #     "email" : "supervsioruser@gmail.com",
            #     "password" : "Abcd.1234",
            #     "phone_number" : "6574120932"
            # },
            # {
            #     "username" : "fo user",
            #     "login_id" : "fouser",
            #     "email" : "fouser@gmail.com",
            #     "password" : "Abcd.1234",
            #     "phone_number" : "6574120931"
            # },
            # {
            #     "username": "monica fo user",
            #     "login_id": "monicafofouser",
            #     "email": "monicafofouser@gmail.com",
            #     "password": "Abcd.1234",
            #     "phone_number": "2574120931",
            # }
        ]

    def handle(self, *args, **kwargs) -> None:
        """
        Main method to load users into the system.
        Handles user creation, user detail setup, role assignment, and sends credentials via email.
        """
        self.stdout.write(self.style.NOTICE("Starting user loading process..."))

        User = get_user_model()
        users_data: List[Dict[str, Any]] = self.get_load_user_data()

        project_name: str = PROJECT_NAME
        project_url: str = FRONTEND_URL

        for user_data in users_data:
            with transaction.atomic():
                login_id: str = user_data["login_id"]
                email: str = user_data["email"]
                password: str = user_data["password"]
                phone_number: str = user_data["phone_number"]
                username: str = user_data["username"]

                # Hardcoding ADMIN role for all users
                role_enum: UserRoleEnum = UserRoleEnum.ADMIN

                # Get or create the user role
                user_role, _ = UserRoleModel.objects.get_or_create(
                    role=role_enum.value,
                    defaults={
                        "id": uuid1(),
                        "title": role_enum.value,
                    },
                )

                # Get or create the user
                user, created = User.objects.get_or_create(
                    login_id=login_id,
                    defaults={
                        "id": uuid1(),
                        "username": username,
                        "email": email,
                        "phone_number": phone_number,
                        "user_role": user_role,
                        "is_active": True,
                        "is_approved": True,
                        "is_verified": True,
                        "is_staff": role_enum == UserRoleEnum.ADMIN,
                        "is_superuser": role_enum == UserRoleEnum.ADMIN,
                    },
                )

                if created:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"User created: {login_id}"))
                else:
                    self.stdout.write(
                        self.style.WARNING(f"User already exists: {login_id}")
                    )

                # Get or create user detail entry
                UserDetailModel.objects.get_or_create(user=user)

                # Prepare email content
                subject: str = f"[{project_name}] Your Account Details"
                body: str = f"""
                    <p>Dear {username},</p>
                    <p>Your account for <strong>{project_name}</strong> has been created.</p>
                    <p><strong>Login ID:</strong> {login_id}<br>
                    <strong>Email:</strong> {email}<br>
                    <strong>Password:</strong> {password}</p>
                    <p>You can access the platform here: <a href="{project_url}">{project_url}</a></p>
                    <p>Regards,<br/>SigmaTech Team</p>
                """

                # # Send the email with credentials
                # success, message = send_an_email(
                #     receiver_email=email, subject=subject, body=body
                # )

                # if success:
                #     self.stdout.write(self.style.SUCCESS(f"Email sent to: {email}"))
                # else:
                #     self.stdout.write(
                #         self.style.ERROR(f"Failed to send email to {email}: {message}")
                #     )

        self.stdout.write(self.style.SUCCESS("User loading process complete."))
