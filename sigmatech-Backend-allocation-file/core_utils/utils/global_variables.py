from core_utils.utils.enums import CoreUtilsStatusEnum
from user_config.user_auth.enums import UserRoleEnum


STATUS_ACTIVATED_GLOBAL_FILTERSET: dict = {
    "status": CoreUtilsStatusEnum.ACTIVATED.value
}


USER_MODEL_EXCLUDE_ADMIN_ROLE_FILTERSET: dict = {
    "user_role__role": UserRoleEnum.ADMIN.value
}
