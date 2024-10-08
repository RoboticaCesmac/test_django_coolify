import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Kid

user_model = get_user_model()


@pytest.mark.django_db
def test_signal_active_kid():
    user = get_user_model().objects.create(username="testuser")
    kid_1 = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    kid_2 = Kid.objects.create(name="Josh", birth_date="1990-01-01", father=user)

    user.profile.is_active = False
    user.profile.save()
    assert not Kid.objects.get(pk=kid_1.pk).is_active
    assert not Kid.objects.get(pk=kid_2.pk).is_active


@pytest.mark.django_db
def test_signal_active_kids_not_exists():
    user = get_user_model().objects.create(username="testuser")

    user.profile.is_active = False
    user.profile.save()


@pytest.mark.django_db
def test_create_kid(api_client):
    user = get_user_model().objects.get(username="testuser")
    data = {
        "name": "John",
        "birth_date": "2017-01-01",
    }

    response = api_client.post(f"{reverse('kid-list')}", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert user.kids.count() == 1


@pytest.mark.django_db
def test_get_kids(api_client):
    user = get_user_model().objects.get(username="testuser")
    Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    Kid.objects.create(
        name="John", birth_date="1990-01-01", father=user, is_active=False
    )

    response = api_client.get(f"{reverse('kid-list')}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_kid(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    data = {"name": "John Doe", "birth_date": "2017-01-01"}

    response = api_client.put(f"{reverse('kid-detail', kwargs={'pk': kid.pk})}", data)

    assert response.status_code == status.HTTP_200_OK
    assert Kid.objects.get(pk=kid.pk).name == "John Doe"
    assert Kid.objects.get(pk=kid.pk).birth_date.isoformat() == "2017-01-01"


@pytest.mark.django_db
def test_delete_kid(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)

    response = api_client.delete(f"{reverse('kid-detail', kwargs={'pk': kid.pk})}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kid.objects.filter(pk=kid.pk).exists()
    assert not Kid.objects.get(pk=kid.pk).is_active
