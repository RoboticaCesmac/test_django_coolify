from core.schema import DynamicFieldsModelSerializer
from .models import (
    DiaphragmaticBreathing,
    TutorialDiaphragmaticBreathing,
)


class DiaphragmaticBreathingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DiaphragmaticBreathing
        fields = ["id", "appointment", "date", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class TutorialDiaphragmaticBreathingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TutorialDiaphragmaticBreathing
        fields = ["id", "step", "image", "audio", "created_at", "updated_at"]
        read_only_fields = ["id", "step", "image", "audio", "created_at", "updated_at"]
