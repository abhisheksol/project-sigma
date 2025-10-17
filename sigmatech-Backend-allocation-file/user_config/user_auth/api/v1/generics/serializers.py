from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserAuthUserListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "login_id"]



from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
from rest_framework import serializers
from user_config.user_auth.models import FoAttendanceModel
from user_config.user_auth.api.v1.generics.handler import FoAttendanceUpdateHandler
from rest_framework import serializers
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin
 
from datetime import datetime
 
 
class FoAttendanceListSerializerModel(CoreGenericSerializerMixin, serializers.ModelSerializer):
    hours_worked = serializers.SerializerMethodField()
 
    class Meta:
        model = FoAttendanceModel
        fields = [
            "id",
            "fo_user",
            "date",
            "duty_on",
            "duty_off",
            "hours_worked",
            "fo_status",
        ]
 
    def get_hours_worked(self, obj):
        if obj.duty_on and obj.duty_off:
            delta = datetime.combine(
                obj.date, obj.duty_off) - datetime.combine(obj.date, obj.duty_on)
            return round(delta.total_seconds() / 3600, 2)
        return 0
 
 
class FoAtttancePutSerializerModel(
    CoreGenericSerializerMixin, serializers.Serializer
):
    fo_status = serializers.CharField(required=False)
    handler_class = FoAttendanceUpdateHandler
    queryset = FoAttendanceModel.objects.all()
 