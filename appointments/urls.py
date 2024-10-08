from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAppointmentView

router = DefaultRouter()
router.register(r"", UserAppointmentView)


user_urlpatterns = [
    path("me/kids/<int:kid_pk>/appointments/", include(router.urls)),
]
