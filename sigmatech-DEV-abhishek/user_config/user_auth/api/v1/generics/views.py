from core_utils.utils.generics.views.generic_views import CoreGenericListAPIView
from .serializers import UserAuthUserListModelSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model


class UserAuthUserListModelAPIView(
    CoreGenericListAPIView,
    generics.ListAPIView,
):
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        serializer_class = {
            "GET": UserAuthUserListModelSerializer,
        }
        return serializer_class.get(self.request.method)
