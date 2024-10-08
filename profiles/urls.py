from django.urls import path
from .views import UserProfileDetailView

user_urlpatterns = [
    path(
        "me/profiles/",
        UserProfileDetailView.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="profile-detail",
    ),
]
