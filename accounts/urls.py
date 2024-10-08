from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserView, UserDetailView

router = DefaultRouter()
router.register(r"", UserView, basename="user")

urlpatterns = [
    path(
        "me/",
        UserDetailView.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="user-detail",
    ),
]

urlpatterns += router.urls
