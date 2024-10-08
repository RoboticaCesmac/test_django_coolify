import pytest
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from kids.models import Kid
from appointments.models import Appointment
from .models import (
    DiaphragmaticBreathing,
    TutorialDiaphragmaticBreathing,
)

user_model = get_user_model()


@pytest.mark.django_db
def test_signal_active_diaphragmatic_breathing():
    user = get_user_model().objects.create(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    diaphragmatic_breathing_1 = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment
    )
    diaphragmatic_breathing_2 = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment
    )

    appointment.is_active = False
    appointment.save()
    assert not DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing_1.pk
    ).is_active
    assert not DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing_2.pk
    ).is_active


@pytest.mark.django_db
def test_signal_active_diaphragmatic_breathing_not_exists():
    user = get_user_model().objects.create(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    appointment.is_active = False
    appointment.save()


@pytest.mark.django_db
def test_create_diaphragmatic_breathing(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "date": date.isoformat(),
    }

    response = api_client.post(
        f"{reverse('diaphragmaticbreathing-list', kwargs={'kid_pk' : kid.pk, 'appointment_pk' : appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert appointment.diaphragmatic_breathings.count() == 1


@pytest.mark.django_db
def test_get_kid_not_found(api_client):
    user = get_user_model().objects.create(
        username="testuser1", password="testpassword"
    )
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "appointment": appointment.pk,
        "date": date.isoformat(),
    }

    response = api_client.post(
        f"{reverse('diaphragmaticbreathing-list', kwargs={'kid_pk' : kid.pk, 'appointment_pk': appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Kid" in response.data["detail"]


@pytest.mark.django_db
def test_get_appointment_not_found(api_client):
    # User Kid
    api_user = get_user_model().objects.get(username="testuser")
    api_user_kid = Kid.objects.create(
        name="John", birth_date="1990-01-01", father=api_user
    )

    # Other user appointment
    user = get_user_model().objects.create(
        username="testuser1", password="testpassword"
    )
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "appointment": appointment.pk,
        "date": date.isoformat(),
    }

    response = api_client.post(
        f"{reverse('diaphragmaticbreathing-list', kwargs={'kid_pk' : api_user_kid.pk, 'appointment_pk': appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Appointment" in response.data["detail"]


@pytest.mark.django_db
def test_get_diaphragmatic_breathings(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    DiaphragmaticBreathing.objects.create(date=timezone.now(), appointment=appointment)
    DiaphragmaticBreathing.objects.create(date=timezone.now(), appointment=appointment)
    DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment, is_active=False
    )

    response = api_client.get(
        f"{reverse('diaphragmaticbreathing-list', kwargs={'kid_pk' : kid.pk, 'appointment_pk': appointment.pk})}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_diaphragmatic_breathing(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    diaphragmatic_breathing = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment
    )

    date = timezone.now() + datetime.timedelta(days=50)
    data = {
        "appointment": appointment.pk,
        "date": date.isoformat(),
    }

    response = api_client.put(
        f"{reverse('diaphragmaticbreathing-detail', kwargs={'kid_pk': kid.pk, 'appointment_pk': appointment.pk, 'pk' : diaphragmatic_breathing.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        DiaphragmaticBreathing.objects.get(pk=diaphragmatic_breathing.pk).appointment.pk
        == appointment.pk
    )
    assert (
        DiaphragmaticBreathing.objects.get(pk=diaphragmatic_breathing.pk).date == date
    )


@pytest.mark.django_db
def test_partial_update_diaphragmatic_breathing(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    diaphragmatic_breathing = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment
    )
    date = timezone.now() + datetime.timedelta(days=50)

    data = {"date": timezone.now() + datetime.timedelta(days=50)}

    response = api_client.patch(
        f"{reverse('diaphragmaticbreathing-detail', kwargs={'kid_pk': kid.pk, 'appointment_pk': appointment.pk, 'pk' : diaphragmatic_breathing.pk})}",
        data,
    )

    print(DiaphragmaticBreathing.objects.get(pk=diaphragmatic_breathing.pk).date)

    assert response.status_code == status.HTTP_200_OK
    assert (
        DiaphragmaticBreathing.objects.get(pk=diaphragmatic_breathing.pk).appointment.pk
        == appointment.pk
    )
    assert DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing.pk
    ).date.isoformat(timespec="minutes") == date.isoformat(timespec="minutes")


@pytest.mark.django_db
def test_update_other_user_diaphragmatic_breathing(api_client):
    # Checks if its possible to update an diaphragmatic breathing to be from another user kids appointment
    client_user = get_user_model().objects.get(username="testuser")
    client_user_kid = Kid.objects.create(
        name="John", birth_date="1990-01-01", father=client_user
    )
    client_user_appointment = Appointment.objects.create(
        kid=client_user_kid, doctor="Dr. Smith", date=timezone.now()
    )
    client_user_diaphragmatic_breathing = DiaphragmaticBreathing.objects.create(
        appointment=client_user_appointment, date=timezone.now()
    )

    user = get_user_model().objects.create(
        username="testuser1", password="testpassword"
    )
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    date = timezone.now() + datetime.timedelta(days=1)
    data = {"appointment": appointment.pk, "date": date.isoformat()}

    response = api_client.put(
        f"{reverse('diaphragmaticbreathing-detail', kwargs={'kid_pk': client_user_kid.pk, 'appointment_pk' : client_user_appointment.pk, 'pk' : client_user_diaphragmatic_breathing.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Appointment" in response.data["detail"]


@pytest.mark.django_db
def test_delete_diaphragmatic_breathing(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    diaphragmatic_breathing = DiaphragmaticBreathing.objects.create(
        date=timezone.now(), appointment=appointment
    )

    response = api_client.delete(
        f"{reverse('diaphragmaticbreathing-detail', kwargs={'kid_pk': kid.pk, 'appointment_pk' : appointment.pk, 'pk' : diaphragmatic_breathing.pk})}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert DiaphragmaticBreathing.objects.filter(pk=diaphragmatic_breathing.pk).exists()
    assert not DiaphragmaticBreathing.objects.get(
        pk=diaphragmatic_breathing.pk
    ).is_active


@pytest.mark.django_db
def test_tutorial_diaphragmatic_breathing(api_client):
    TutorialDiaphragmaticBreathing.objects.create(
        step=3, image="image3.jpg", audio="audio3.mp3"
    )
    TutorialDiaphragmaticBreathing.objects.create(
        step=2, image="image2.jpg", audio="audio2.mp3"
    )
    TutorialDiaphragmaticBreathing.objects.create(
        step=1, image="image1.jpg", audio="audio1.mp3"
    )

    response = api_client.get(f"{reverse('tutorial-diaphragmatic-breathing-list')}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]["step"] == 1
    assert "audio1.mp3" in response.data[0]["audio"]
    assert "image1.jpg" in response.data[0]["image"]
