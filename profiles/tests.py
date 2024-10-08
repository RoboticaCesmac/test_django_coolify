import pytest
import datetime
from freezegun import freeze_time
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer


@pytest.mark.django_db
def test_signal_create_profile():
    user = get_user_model().objects.create(username="testuser")
    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_signal_active_profile():
    user = get_user_model().objects.create(username="testuser")

    user.is_active = False
    user.save()
    assert not Profile.objects.get(user=user).is_active

    user.is_active = True
    user.save()
    assert Profile.objects.get(user=user).is_active


@pytest.mark.django_db
def test_profile_serializer():
    user = get_user_model().objects.create(username="testuser")

    profile_serializer = ProfileSerializer(instance=user.profile)

    assert profile_serializer.data["user"]["username"] == user.username


@pytest.mark.django_db
@freeze_time("2020-01-01")
def test_age():
    user = get_user_model().objects.create(username="testuser")

    user.profile.birth_date = datetime.date(1990, 1, 1)
    user.profile.save()
    profile_serializer = ProfileSerializer(instance=user.profile)

    assert profile_serializer.data["age"] == 30


@pytest.mark.django_db
def test_profile_detail_view(api_client):

    response = api_client.get(f"{reverse('profile-detail')}", format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["username"] == "testuser"
    assert response.data["user"]["full_name"] == "Test User"
    assert response.data["birth_date"] is None
    assert response.data["age"] is None


@pytest.mark.django_db
def test_profile_partial_update_view(api_client):
    response = api_client.patch(
        f"{reverse('profile-detail')}",
        data={
            "user": {"first_name": "leonardo", "last_name": "Carlos Roberto"},
            "birth_date": "1990-01-01",
        },
        format="json",
    )
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["username"] == "testuser"
    assert response.data["user"]["full_name"] == "leonardo Carlos Roberto"
    assert response.data["user"]["first_name"] == "leonardo"
    assert response.data["user"]["last_name"] == "Carlos Roberto"
    assert response.data["birth_date"] == "1990-01-01"
    assert int(response.data["age"])


@pytest.mark.django_db
def test_profile_partial_update_view_without_user(api_client):
    response = api_client.patch(
        f"{reverse('profile-detail')}",
        data={
            "birth_date": "1990-01-01",
        },
        format="json",
    )
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["username"] == "testuser"
    assert response.data["user"]["full_name"] == "Test User"
    assert response.data["user"]["first_name"] == "Test"
    assert response.data["user"]["last_name"] == "User"
    assert response.data["birth_date"] == "1990-01-01"
    assert int(response.data["age"])


@pytest.mark.django_db
def test_birth_date_validator(api_client):
    future = datetime.date.today() + datetime.timedelta(days=1)
    print(future.isoformat())
    response = api_client.patch(
        f"{reverse('profile-detail')}",
        data={"birth_date": future.isoformat()},
        format="json",
    )
    print(response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["birth_date"][0].code == "invalid"
