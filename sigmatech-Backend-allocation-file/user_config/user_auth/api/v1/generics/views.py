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


from core_utils.utils.generics.views.generic_views import (
    CoreGenericGetAPIView,
    CoreGenericPutAPIView,
    CoreGenericDeleteAPIView,
)
from rest_framework import generics, permissions
from user_config.user_auth.models import FoAttendanceModel
from user_config.user_auth.utils.custom_authentication.custom_authentication import (
    CustomAuthentication)
from user_config.user_auth.api.v1.generics.serializers import (
    FoAttendanceListSerializerModel, FoAtttancePutSerializerModel)
 
 
class FoOperationsAttendanceGetAPIView(
    CoreGenericGetAPIView,
    CoreGenericDeleteAPIView,
    CoreGenericPutAPIView,
    generics.GenericAPIView,
 
):
    queryset = FoAttendanceModel.objects.all()
    authentication_classes = [CustomAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        queryset = self.queryset
        attendance_id = self.request.query_params.get('fo_user')
        print("attendance_id", attendance_id)
        if attendance_id:
            queryset = queryset.filter(fo_user__id=attendance_id)
            print("queryset--->", queryset)
        return queryset
 
    def get_serializer_class(self):
        return {
            'GET': FoAttendanceListSerializerModel,
            'PUT': FoAtttancePutSerializerModel
        }.get(self.request.method)
 