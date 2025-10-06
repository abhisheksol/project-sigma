from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetDataFromSerializerAPIView,
)
from rest_framework import generics, permissions
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)
from .serializers import EnumHelperHelperListSerializer


class EnumsHelperListAPIView(
    CoreGenericGetDataFromSerializerAPIView, generics.GenericAPIView
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return {
            "GET": EnumHelperHelperListSerializer,
        }.get(self.request.method)
