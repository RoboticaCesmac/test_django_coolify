from rest_framework import viewsets, permissions
from django.utils.translation import gettext_lazy as _
from .models import Kid
from .serializers import KidSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema(tags=["kids"])
@extend_schema_view(
    list=extend_schema(summary=_("Retrieve all kids belonging to the current user.")),
    create=extend_schema(summary=_("Create a new kid for the current user.")),
    retrieve=extend_schema(
        summary=_("Retrieve a specific kid belonging to the current user.")
    ),
    update=extend_schema(
        summary=_("Update a specific kid belonging to the current user.")
    ),
    partial_update=extend_schema(
        summary=_("Partially update a specific kid belonging to the current user.")
    ),
    destroy=extend_schema(
        summary=_("Delete a specific kid belonging to the current user.")
    ),
)
class UserKidsView(viewsets.ModelViewSet):

    queryset = Kid.active_objects.all()
    serializer_class = KidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the kids belonging to the authenticated user."""
        return self.queryset.filter(father=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
