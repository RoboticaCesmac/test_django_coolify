from rest_framework import viewsets, permissions, mixins, response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .serializers import UserSerializer, UserPatchSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

user_model = get_user_model()


@extend_schema_view(create=extend_schema(summary=_("Register a new user")))
class UserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = UserSerializer


class UserDetailView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        summary=_("Returns the currently logged-in user."),
    )
    def retrieve(self, request):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data)

    @extend_schema(
        summary=_("Partially update the logged-in user."), request=UserPatchSerializer
    )
    def partial_update(self, request):
        serializer = UserPatchSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(self.serializer_class(request.user).data)
