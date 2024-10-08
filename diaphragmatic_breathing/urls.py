from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserDiaphragmaticBreathingView,
    TutorialDiaphragmaticBreathingView,
)

router = DefaultRouter()
router.register(r"", UserDiaphragmaticBreathingView)

user_urlpatterns = [
    path(
        "me/kids/<int:kid_pk>/appointments/<int:appointment_pk>/diaphragmatic-breathing/",
        include(router.urls),
    ),
]

tutorial_urlpatterns = [
    path(
        "tutorial-diaphragmatic-breathing/",
        TutorialDiaphragmaticBreathingView.as_view(),
        name="tutorial-diaphragmatic-breathing-list",
    ),
]
