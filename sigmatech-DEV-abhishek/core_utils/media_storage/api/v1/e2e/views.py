from rest_framework import generics, permissions
from core_utils.utils.generics.views.generic_views import CoreGenericPostAPIView
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class FileToUrlConversionAPIView(CoreGenericPostAPIView, generics.GenericAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = {"POST": None}

        return serializer_class.get(self.request.method)
