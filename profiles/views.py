from rest_framework import viewsets, permissions, response
from django.utils.translation import gettext_lazy as _
from .serializers import ProfileSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["profiles"])
class UserProfileDetailView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    @extend_schema(summary=_("Retrieve current logged user and their profile details."))
    def retrieve(self, request):
        serializer = self.serializer_class(request.user.profile)
        return response.Response(serializer.data)

    @extend_schema(
        summary=_(
            "Partially update the birth date, user first name and user last name in the profile of the current logged user."
        )
    )
    def partial_update(self, request):

        serializer = self.serializer_class(
            request.user.profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
