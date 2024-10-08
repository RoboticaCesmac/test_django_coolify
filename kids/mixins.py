from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from .models import Kid


class GetKidMixin:
    """Mixin to retrieve the kid associated with the user."""

    def get_kid(self, pk=None):
        """Check if the kid belongs to the user and return the kid's id."""
        kid_pk = pk or self.kwargs["kid_pk"]
        try:
            kid = Kid.objects.get(father=self.request.user, id=kid_pk)
        except Kid.DoesNotExist as exc:
            raise exceptions.NotFound(_("Kid not found")) from exc
        return kid.pk
