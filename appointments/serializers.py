from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from django.utils.translation import gettext as _
from .models import Appointment


class AppointmentSerializer(DynamicFieldsModelSerializer):
    diaphragmatic_breathings_made = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        if attrs.get("score", None):
            status = attrs.get("status", None) or self.instance.status
            if status and status.lower() == "pending":
                raise serializers.ValidationError(
                    _("Score can only be added to completed appointments.")
                )
        return attrs

    class Meta:
        model = Appointment
        fields = [
            "id",
            "kid",
            "doctor",
            "date",
            "status",
            "score",
            "diaphragmatic_breathings_made",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "diaphragmatic_breathings_made",
        ]
