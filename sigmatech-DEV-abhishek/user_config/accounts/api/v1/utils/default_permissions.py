from user_config.user_auth.enums import UserRoleEnum

DEFAULT_PERMISSIONS_TO_USER_ROLE: dict = {
    UserRoleEnum.SR_MANAGER.value: [
        {
            "id": "e34ab39b-7e85-11f0-908a-00155d4d8337",
            "title": "Process Configurations",
            "sub_permissions": [
                {
                    "id": "ec9f6145-7e85-11f0-83dd-00155d4d8337",
                    "title": "Process Management",
                    "has_access": True,
                },
                {
                    "id": "094b8491-7e86-11f0-baf7-00155d4d8337",
                    "title": "Product Management",
                    "has_access": True,
                },
                {
                    "id": "0580c888-7e87-11f0-bb9c-00155d4d8337",
                    "title": "Buckets Management",
                    "has_access": True,
                },
                {
                    "id": "0ec80778-7e87-11f0-8ea7-00155d4d8337",
                    "title": "Cycles Management",
                    "has_access": True,
                },
            ],
        },
        {
            "id": "1b11da24-7e87-11f0-a3ad-00155d4d8337",
            "title": "Region Configurations",
            "sub_permissions": [
                {
                    "id": "314c6768-7e87-11f0-983c-00155d4d8337",
                    "title": "Manage Regions",
                    "has_access": True,
                },
                {
                    "id": "3d7832c3-7e87-11f0-bf35-00155d4d8337",
                    "title": "Manage Zones",
                    "has_access": True,
                },
                {
                    "id": "476b848b-7e87-11f0-8cae-00155d4d8337",
                    "title": "Manage City/Area",
                    "has_access": False,
                },
                {
                    "id": "4ee83a8a-7e87-11f0-9c0f-00155d4d8337",
                    "title": "Manage Pin Codes",
                    "has_access": False,
                },
                {
                    "id": "122a33bc-7e98-11f0-9ad3-00155d4d8337",
                    "title": "Manage Sub-area",
                    "has_access": True,
                },
            ],
        },
        {
            "id": "1ff5e6a0-7e98-11f0-949f-00155d4d8337",
            "title": "User Management",
            "sub_permissions": [
                {
                    "id": "3548b721-7e98-11f0-aa67-00155d4d8337",
                    "title": "User Accounts",
                    "has_access": True,
                }
            ],
        },
    ],
    UserRoleEnum.MANAGER.value: [
        {
            "id": "e34ab39b-7e85-11f0-908a-00155d4d8337",
            "title": "Process Configurations",
            "sub_permissions": [
                {
                    "id": "ec9f6145-7e85-11f0-83dd-00155d4d8337",
                    "title": "Process Management",
                    "has_access": True,
                },
                {
                    "id": "094b8491-7e86-11f0-baf7-00155d4d8337",
                    "title": "Product Management",
                    "has_access": True,
                },
                {
                    "id": "0580c888-7e87-11f0-bb9c-00155d4d8337",
                    "title": "Buckets Management",
                    "has_access": True,
                },
                {
                    "id": "0ec80778-7e87-11f0-8ea7-00155d4d8337",
                    "title": "Cycles Management",
                    "has_access": True,
                },
            ],
        },
        {
            "id": "1b11da24-7e87-11f0-a3ad-00155d4d8337",
            "title": "Region Configurations",
            "sub_permissions": [
                {
                    "id": "314c6768-7e87-11f0-983c-00155d4d8337",
                    "title": "Manage Regions",
                    "has_access": True,
                },
                {
                    "id": "3d7832c3-7e87-11f0-bf35-00155d4d8337",
                    "title": "Manage Zones",
                    "has_access": True,
                },
                {
                    "id": "476b848b-7e87-11f0-8cae-00155d4d8337",
                    "title": "Manage City/Area",
                    "has_access": False,
                },
                {
                    "id": "4ee83a8a-7e87-11f0-9c0f-00155d4d8337",
                    "title": "Manage Pin Codes",
                    "has_access": False,
                },
                {
                    "id": "122a33bc-7e98-11f0-9ad3-00155d4d8337",
                    "title": "Manage Sub-area",
                    "has_access": True,
                },
            ],
        },
        {
            "id": "1ff5e6a0-7e98-11f0-949f-00155d4d8337",
            "title": "User Management",
            "sub_permissions": [
                {
                    "id": "3548b721-7e98-11f0-aa67-00155d4d8337",
                    "title": "User Accounts",
                    "has_access": True,
                }
            ],
        },
    ],
    UserRoleEnum.SUPERVISOR.value: [
        {
            "id": "e34ab39b-7e85-11f0-908a-00155d4d8337",
            "title": "Process Configurations",
            "sub_permissions": [
                {
                    "id": "ec9f6145-7e85-11f0-83dd-00155d4d8337",
                    "title": "Process Management",
                    "has_access": False,
                },
                {
                    "id": "094b8491-7e86-11f0-baf7-00155d4d8337",
                    "title": "Product Management",
                    "has_access": False,
                },
                {
                    "id": "0580c888-7e87-11f0-bb9c-00155d4d8337",
                    "title": "Buckets Management",
                    "has_access": False,
                },
                {
                    "id": "0ec80778-7e87-11f0-8ea7-00155d4d8337",
                    "title": "Cycles Management",
                    "has_access": False,
                },
            ],
        },
        {
            "id": "1b11da24-7e87-11f0-a3ad-00155d4d8337",
            "title": "Region Configurations",
            "sub_permissions": [
                {
                    "id": "314c6768-7e87-11f0-983c-00155d4d8337",
                    "title": "Manage Regions",
                    "has_access": False,
                },
                {
                    "id": "3d7832c3-7e87-11f0-bf35-00155d4d8337",
                    "title": "Manage Zones",
                    "has_access": False,
                },
                {
                    "id": "476b848b-7e87-11f0-8cae-00155d4d8337",
                    "title": "Manage City/Area",
                    "has_access": True,
                },
                {
                    "id": "4ee83a8a-7e87-11f0-9c0f-00155d4d8337",
                    "title": "Manage Pin Codes",
                    "has_access": True,
                },
                {
                    "id": "122a33bc-7e98-11f0-9ad3-00155d4d8337",
                    "title": "Manage Sub-area",
                    "has_access": True,
                },
            ],
        },
        {
            "id": "1ff5e6a0-7e98-11f0-949f-00155d4d8337",
            "title": "User Management",
            "sub_permissions": [
                {
                    "id": "3548b721-7e98-11f0-aa67-00155d4d8337",
                    "title": "User Accounts",
                    "has_access": True,
                }
            ],
        },
    ],
    UserRoleEnum.FIELD_OFFICER.value: [
        {
            "id": "e34ab39b-7e85-11f0-908a-00155d4d8337",
            "title": "Process Configurations",
            "sub_permissions": [
                {
                    "id": "ec9f6145-7e85-11f0-83dd-00155d4d8337",
                    "title": "Process Management",
                    "has_access": False,
                },
                {
                    "id": "094b8491-7e86-11f0-baf7-00155d4d8337",
                    "title": "Product Management",
                    "has_access": False,
                },
                {
                    "id": "0580c888-7e87-11f0-bb9c-00155d4d8337",
                    "title": "Buckets Management",
                    "has_access": False,
                },
                {
                    "id": "0ec80778-7e87-11f0-8ea7-00155d4d8337",
                    "title": "Cycles Management",
                    "has_access": False,
                },
            ],
        },
        {
            "id": "1b11da24-7e87-11f0-a3ad-00155d4d8337",
            "title": "Region Configurations",
            "sub_permissions": [
                {
                    "id": "314c6768-7e87-11f0-983c-00155d4d8337",
                    "title": "Manage Regions",
                    "has_access": False,
                },
                {
                    "id": "3d7832c3-7e87-11f0-bf35-00155d4d8337",
                    "title": "Manage Zones",
                    "has_access": False,
                },
                {
                    "id": "476b848b-7e87-11f0-8cae-00155d4d8337",
                    "title": "Manage City/Area",
                    "has_access": False,
                },
                {
                    "id": "4ee83a8a-7e87-11f0-9c0f-00155d4d8337",
                    "title": "Manage Pin Codes",
                    "has_access": False,
                },
                {
                    "id": "122a33bc-7e98-11f0-9ad3-00155d4d8337",
                    "title": "Manage Sub-area",
                    "has_access": False,
                },
            ],
        },
        {
            "id": "1ff5e6a0-7e98-11f0-949f-00155d4d8337",
            "title": "User Management",
            "sub_permissions": [
                {
                    "id": "3548b721-7e98-11f0-aa67-00155d4d8337",
                    "title": "User Accounts",
                    "has_access": False,
                }
            ],
        },
    ],
}
