from core_utils.utils.constant import (
    MANAGE_COLUMNS_API_SUCCESS_MESSAGE,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)

# from ..models import UserConfigTableOrderModel, UserConfigTableFieldsModel
# from accounts.models import AccountsUserDetailsModel


from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetDataFromSerializerAPIView,
    CoreGenericPostAPIView,
)


from .serializers import (
    GenericUserConfigTableOrderSerializer,
    GenericUserConfigTableOrderPostSerializer,
)
from rest_framework import generics, permissions


# from core.utils.authentications import CustomAuthentication
import logging
from core_utils.manage_columns.models import (
    CoreUtilsFeaturesModel,
    UserConfigTableFieldsModel,
)

# from core_utils.utils.generics.manage_column.v1.filters import

# from core_utils.utils.generics.manage_column.v1.utils.filters import UserConfigGenericTableFieldsModelFilterSet


class GenericUserConfigManageColumnAPIView(
    CoreGenericGetDataFromSerializerAPIView,
    CoreGenericPostAPIView,
    generics.GenericAPIView,
):
    """
    API to manage user column preferences for a given feature.
    """

    queryset = UserConfigTableFieldsModel.objects.select_related(
        "table__user", "table__feature"
    ).all()

    feature_queryset = CoreUtilsFeaturesModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomAuthentication]
    success_message = MANAGE_COLUMNS_API_SUCCESS_MESSAGE

    logger = logging.LoggerAdapter(
        logging.getLogger(__name__),
        {"app_name": "GenericUserConfigManageColumnAPIView"},
    )

    def get_serializer_class(self):
        """
        Return serializer class based on HTTP method.
        """
        return {
            "GET": GenericUserConfigTableOrderSerializer,
            "POST": GenericUserConfigTableOrderPostSerializer,
        }.get(self.request.method)
