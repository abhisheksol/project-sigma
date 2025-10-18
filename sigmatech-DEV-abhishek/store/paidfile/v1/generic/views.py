from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend

from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication,
)

from store.paidfile.models import paidfile
from store.paidfile.v1.generic.serializers import (
    PaidfileCreateSerializer,
    PaidfileListSerializer,
)
class PaidfileListingGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
    ):

    queryset= paidfile.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    def get_serializer_class(self):
        return {
            "GET": PaidfileListSerializer,
            "POST": PaidfileCreateSerializer,
        }.get(self.request.method)

