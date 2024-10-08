import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from profiles.models import Profile
from kids.models import Kid
from appointments.models import Appointment
from diaphragmatic_breathing.models import DiaphragmaticBreathing
from .models import User
from .serializers import UserSerializer


client = APIClient()


@pytest.mark.django_db
def test_user_inactivate_full_signals_path():
    user = get_user_model().objects.create(username="testuser")
    kid_1 = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    kid_2 = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment_1 = Appointment.objects.create(
        kid=kid_1, doctor="Dr. Smith", date=timezone.now()
    )
    appointment_2 = Appointment.objects.create(
        kid=kid_2, doctor="Dr. Smith", date=timezone.now()
    )
    diaphragmatic_breathing_1 = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment_1
    )
    diaphragmatic_breathing_2 = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment_2
    )

    user.is_active = False
    user.save()

    assert not Profile.objects.get(user=user).is_active
    assert not Kid.objects.get(pk=kid_1.pk).is_active
    assert not Kid.objects.get(pk=kid_2.pk).is_active
    assert not Appointment.objects.get(pk=appointment_1.pk).is_active
    assert not Appointment.objects.get(pk=appointment_2.pk).is_active
    assert not DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing_1.pk
    ).is_active
    assert not DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing_2.pk
    ).is_active


@pytest.mark.django_db
def test_user_serializer_create():
    user_data = {
        "username": "leonardo",
        "password": "teste",
        "first_name": "Joazinho",
        "last_name": "Testinho Teste",
    }
    serializer = UserSerializer(data=user_data)
    serializer.is_valid()
    user = serializer.save()

    assert user.username == "leonardo"
    assert user.first_name == "Joazinho"
    assert user.last_name == "Testinho Teste"


@pytest.mark.django_db
def test_user_serializer_full_name():
    user_data = {
        "username": "leonardo",
        "password": "teste",
        "first_name": "Joazinho",
        "last_name": "Testinho Teste",
    }
    full_name = f"{user_data['first_name']} {user_data['last_name']}"

    serializer = UserSerializer(data=user_data)
    serializer.is_valid()
    serializer.save()

    assert serializer.data["full_name"] == full_name


@pytest.mark.django_db
def test_singup():
    response = client.post(
        f"{reverse('user-list')}",
        {
            "username": "leonardo",
            "password": "teste",
            "first_name": "Joazinho",
            "last_name": "Testinho Teste",
        },
        format="json",
    )

    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED
    assert len(User.objects.filter(is_active=True)) == 1


@pytest.mark.django_db
def test_retrieve(api_client):
    response = api_client.get(
        f"{reverse('user-detail')}",
        format="json",
    )
    print(response.data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_partial_update(api_client):
    response = api_client.patch(
        f"{reverse('user-detail')}",
        data={
            "first_name": "Joazinho 123",
            "last_name": "Testinho Teste 123",
        },
        format="json",
    )
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Joazinho 123"
    assert response.data["last_name"] == "Testinho Teste 123"
    assert response.data["full_name"] == "Joazinho 123 Testinho Teste 123"
