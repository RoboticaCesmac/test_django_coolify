import copy
from rest_framework import viewsets, permissions, exceptions, response, status, generics
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from kids.mixins import GetKidMixin
from appointments.models import Appointment
from .serializers import (
    DiaphragmaticBreathingSerializer,
    TutorialDiaphragmaticBreathingSerializer,
)
from .models import (
    DiaphragmaticBreathing,
    TutorialDiaphragmaticBreathing,
)


@extend_schema(tags=["diaphragmatic-breathings"])
@extend_schema_view(
    list=extend_schema(
        summary=_(
            "Retrieve all diaphragmatic breathings from appointments of current user's kids."
        )
    ),
    retrieve=extend_schema(
        summary=_(
            "Retrieve a specific diaphragmatic breathing from an appointment of the current user's kid."
        )
    ),
    partial_update=extend_schema(
        summary=_(
            "Partially update a specific diaphragmatic breathing from an appointment of the current user's kid."
        )
    ),
    destroy=extend_schema(
        summary=_(
            "Delete a specific diaphragmatic breathing from an appointment of the current user's kid."
        )
    ),
)
class UserDiaphragmaticBreathingView(GetKidMixin, viewsets.ModelViewSet):
    serializer_class = DiaphragmaticBreathingSerializer
    queryset = DiaphragmaticBreathing.active_objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(appointment=self.get_appointment())

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def add_url_appointment_to_request_data(self):
        data_copy = copy.deepcopy(self.request.data)
        data_copy["appointment"] = self.get_appointment()
        return data_copy

    @extend_schema(
        summary=_(
            "Create a diaphragmatic breathing for an appointment of the current user's kid."
        ),
        request=DiaphragmaticBreathingSerializer(
            fields=["date"], ref_name="DiaphragmaticBreathingCreate"
        ),
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.add_url_appointment_to_request_data()
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @extend_schema(
        summary=_(
            "Update a specific diaphragmatic breathing from an appointment of the current user's kid."
        ),
        description=_(
            "If the appointment in the serializer is not associated with the user, it will return a 404: Appointment not Found."
        ),
    )
    def update(self, request, *args, **kwargs):
        if request.data.get("appointment", None):
            self.get_appointment(request.data["appointment"])

        return super().update(request, *args, **kwargs)

    def get_appointment(self, pk=None):
        """Check if appointment is associated with the user and return the appointment id."""
        appointment_pk = pk or self.kwargs["appointment_pk"]
        try:
            appointment = Appointment.objects.get(kid=self.get_kid(), id=appointment_pk)
        except Appointment.DoesNotExist as exc:
            raise exceptions.NotFound(_("Appointment not found")) from exc
        return appointment.pk


@extend_schema(tags=["diaphragmatic-breathings"])
@extend_schema_view(
    get=extend_schema(summary=_("Returns tutorial diaphragmatic breathing steps.")),
)
class TutorialDiaphragmaticBreathingView(generics.ListAPIView):
    serializer_class = TutorialDiaphragmaticBreathingSerializer
    queryset = TutorialDiaphragmaticBreathing.active_objects.all()
