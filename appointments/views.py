import datetime
import copy
from rest_framework import viewsets, permissions, exceptions, response, status
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from kids.mixins import GetKidMixin
from .models import Appointment
from .serializers import AppointmentSerializer


@extend_schema(tags=["appointments"])
@extend_schema_view(
    list=extend_schema(
        summary=_("Retrieve all appointments for the current user's kid."),
        parameters=[
            OpenApiParameter(
                name="doctor", description="Doctor's name", type=str, required=False
            ),
            OpenApiParameter(
                name="status",
                description="Appointment status",
                type=str,
                required=False,
            ),
            OpenApiParameter(
                name="date", description="Appointment date", type=str, required=False
            ),
            OpenApiParameter(
                name="score", description="Appointment score", type=int, required=False
            ),
        ],
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific appointment for the current user's kid.")
    ),
    partial_update=extend_schema(
        summary=_("Partially update a specific appointment for the current user's kid.")
    ),
    destroy=extend_schema(
        summary=_("Delete a specific appointment for the current user's kid.")
    ),
)
class UserAppointmentView(GetKidMixin, viewsets.ModelViewSet):
    """If the kid is not associated with the user, it will return a 404: Kid not Found."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    queryset = Appointment.active_objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(kid=self.get_kid())

        status = self.request.query_params.get("status", None)
        doctor = self.request.query_params.get("doctor", None)
        date = self.request.query_params.get("date", None)
        score = self.request.query_params.get("score", None)

        if status:
            queryset = queryset.filter(status=status)
        if doctor:
            queryset = queryset.filter(doctor__contains=doctor)
        if date:
            queryset = queryset.filter(date__date=datetime.datetime.fromisoformat(date))
        if score:
            try:
                queryset = queryset.filter(score=score)
            except ValueError as exc:
                raise exceptions.ParseError(_("Score must be a number")) from exc

        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def add_url_kid_to_request_data(self):
        """Add the url kid to the request data."""
        data_copy = copy.deepcopy(self.request.data)
        data_copy["kid"] = self.get_kid()
        return data_copy

    @extend_schema(
        summary=_("Create an appointment for the current user's kid."),
        request=AppointmentSerializer(
            fields=["doctor", "date", "status", "score"],
            ref_name="AppointmentCreate",  # Kid is still serialized but it will come from the URL
        ),
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.add_url_kid_to_request_data())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @extend_schema(
        summary=_("Update a specific appointment for the current user's kid."),
        description=_(
            "If the kid in the serializer is not associated with the user, it will return a 404: Kid not Found."
        ),
    )
    def update(self, request, *args, **kwargs):
        if request.data.get("kid", None):
            self.get_kid(request.data["kid"])

        return super().update(request, *args, **kwargs)
