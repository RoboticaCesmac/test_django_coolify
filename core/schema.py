from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.utils import Direction
from .serializers import DynamicFieldsModelSerializer


class DynamicFieldsModelSerializerExtension(OpenApiSerializerExtension):
    target_class = DynamicFieldsModelSerializer  # this can also be an import string
    match_subclasses = True

    def map_serializer(self, auto_schema: "AutoSchema", direction: Direction):
        return auto_schema._map_serializer(
            self.target, direction, bypass_extensions=True
        )

    def get_name(self, auto_schema, direction):
        return self.target.ref_name
