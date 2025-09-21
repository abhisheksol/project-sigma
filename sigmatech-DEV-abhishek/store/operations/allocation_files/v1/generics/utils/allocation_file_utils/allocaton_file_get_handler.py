from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler


class AllocationFileHandler(CoreGenericBaseHandler):

    def validate(self):
        pass

    def create(self):
        self.queryset.select_related(
            "cycle",
            "product_assignment",
            "product_assignment__process",
            "product_assignment__product",
        )
