import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

user_model = get_user_model()


@pytest.fixture(autouse=True)
def set_default_language(settings):
    settings.LANGUAGE_CODE = "en"


@pytest.fixture
def api_client():
    user = user_model.objects.create_user(
        username="testuser",
        password="testpassword",
        first_name="Test",
        last_name="User",
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
