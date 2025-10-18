from rest_framework import serializers
from store.paidfile.handlers.paidfile_handler import Paidfilehandler
from store.paidfile.models import paidfile
from core_utils.utils.generics.serializers.mixins import CoreGenericSerializerMixin

class PaidfileListSerializer( CoreGenericSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = paidfile
        fields = ['id', 'loan_account_no', 'payment_mode_code', 'payment_amt','payment_date']


class PaidfileCreateSerializer( CoreGenericSerializerMixin, serializers.ModelSerializer):
    handler_class= Paidfilehandler
    file_path = serializers.CharField(write_only=True)

    class Meta:
        model = paidfile
        fields = ['file_path']
     

