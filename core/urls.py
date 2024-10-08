from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from appointments.urls import user_urlpatterns as user_appointments_urlpatterns
from kids.urls import user_urlpatterns as user_kids_urlpatterns
from profiles.urls import user_urlpatterns as user_profiles_urlpatterns
from diaphragmatic_breathing.urls import (
    user_urlpatterns as user_diaphragmatic_breathing_urlpatterns,
    tutorial_urlpatterns as tutorial_diaphragmatic_breathing_urlpatterns,
)


urlpatterns = [
    # Token Auth
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # API
    path("accounts/", include("accounts.urls")),
    path("accounts/", include(user_appointments_urlpatterns)),
    path("accounts/", include(user_kids_urlpatterns)),
    path("accounts/", include(user_profiles_urlpatterns)),
    path("accounts/", include(user_diaphragmatic_breathing_urlpatterns)),
    path("", include(tutorial_diaphragmatic_breathing_urlpatterns)),
]