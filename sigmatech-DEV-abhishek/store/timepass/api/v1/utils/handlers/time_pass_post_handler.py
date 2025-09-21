from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler

from django.db import transaction

class timepassposthandler(CoreGenericBaseHandler):
    def validate(self):
        pass

    def create(self):
        with transaction.atomic():
            instance = self.queryset.create(**self.data)
            return instance
