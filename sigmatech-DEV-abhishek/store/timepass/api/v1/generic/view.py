
from django.http import HttpResponse
from rest_framework import generics
from store.timepass.api.v1.generic.serializers import Timepassgetserializer
from store.timepass.models import TimepassModel
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from store.timepass.api.v1.generic.serializers import Timepasspostserializer
class CurdGenericAPIView(
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericListCreateAPIView,
    generics.ListCreateAPIView,
    generics.GenericAPIView,
):
    queryset=TimepassModel.objects.all()
    def get_serializer_class(self):
        return {
            "GET": Timepassgetserializer,
            "POST": Timepasspostserializer,
            "PUT": None,
            "DELETE": None,
        }.get(self.request.method)

    
    
