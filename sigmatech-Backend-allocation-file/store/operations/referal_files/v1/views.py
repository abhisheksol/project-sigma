from django.http import HttpResponse
from rest_framework import generics
from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericListCreateAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from rest_framework.response import Response

from store.operations.referal_files.models import ReferalFileModel, FieldOfficerAssignment
# class referral_file_listing(
#      CoreGenericPutAPIView,
#     CoreGenericDeleteAPIView,
#     CoreGenericListCreateAPIView,
#     generics.ListCreateAPIView,
#     generics.GenericAPIView,
# ):
#     print("running get_serializer method............")
#     queryset=FieldOfficerAssignment.objects.all()

#     def get_serializer_class(self):
#         return {
#             "GET": RefferralFileListingModelSerializer,
#         }.get(self.request.method)
        
from rest_framework.generics import ListAPIView
from store.operations.referal_files.models import FieldOfficerAssignment
from store.operations.referal_files.v1.serializers import FieldOfficerListingSerializer

class referral_file_listing(ListAPIView):
    queryset = FieldOfficerAssignment.objects.all()
    serializer_class = FieldOfficerListingSerializer
