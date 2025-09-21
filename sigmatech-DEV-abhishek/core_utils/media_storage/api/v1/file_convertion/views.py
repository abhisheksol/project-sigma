from rest_framework import generics, permissions
from core_utils.media_storage.api.v1.e2e.serializers import (
    FileToUrlConversionModelSerializer,
)
from core_utils.utils.generics.views.generic_views import CoreGenericPostAPIView
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)


class LiveKitFileToUrlConversionAPIView(
    CoreGenericPostAPIView, generics.GenericAPIView
):

    def get_serializer_class(self):
        serializer_class = {"POST": FileToUrlConversionModelSerializer}

        return serializer_class.get(self.request.method)


class FileToUrlConversionAPIView(CoreGenericPostAPIView, generics.GenericAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = {"POST": FileToUrlConversionModelSerializer}

        return serializer_class.get(self.request.method)
