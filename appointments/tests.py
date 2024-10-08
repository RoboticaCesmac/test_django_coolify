import pytest
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from diaphragmatic_breathing.models import DiaphragmaticBreathing
from kids.models import Kid
from .models import Appointment

user_model = get_user_model()


@pytest.mark.django_db
def test_signal_active_appointment():
    user = get_user_model().objects.create(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment_1 = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    appointment_2 = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    kid.is_active = False
    kid.save()
    assert not Appointment.objects.get(pk=appointment_1.pk).is_active
    assert not Appointment.objects.get(pk=appointment_2.pk).is_active


@pytest.mark.django_db
def test_signal_active_appointments_not_exists():
    user = get_user_model().objects.create(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)

    kid.is_active = False
    kid.save()


@pytest.mark.django_db
def test_create_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "doctor": "Dr. Smith",
        "date": date.isoformat(),
        "status": "pending",
    }

    response = api_client.post(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}", data
    )
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert kid.appointments.count() == 1


@pytest.mark.django_db
def test_create_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "kid": 999,
        "doctor": "Dr. Smith",
        "date": date.isoformat(),
        "status": "pending",
    }

    response = api_client.post(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}", data
    )
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["kid"] == kid.pk
    assert kid.appointments.count() == 1


@pytest.mark.django_db
def test_retrieve_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    response = api_client.get(
        f"{reverse('appointment-detail', kwargs={'kid_pk' : kid.pk, 'pk' : appointment.pk})}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["kid"] == kid.pk


@pytest.mark.django_db
def test_diaphragmatic_breathings_made(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    DiaphragmaticBreathing.objects.create(appointment=appointment, date=timezone.now())
    DiaphragmaticBreathing.objects.create(appointment=appointment, date=timezone.now())
    DiaphragmaticBreathing.objects.create(
        appointment=appointment, date=timezone.now(), is_active=False
    )

    response = api_client.get(
        f"{reverse('appointment-detail', kwargs={'kid_pk' : kid.pk, 'pk' : appointment.pk})}"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["diaphragmatic_breathings_made"] == 2


@pytest.mark.django_db
def test_get_kid_not_found(api_client):
    user = get_user_model().objects.create(
        username="testuser1", password="testpassword"
    )
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "kid": kid.pk,
        "doctor": "Dr. Smith",
        "date": date.isoformat(),
        "status": "pending",
    }

    response = api_client.post(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}", data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Kid" in response.data["detail"]


@pytest.mark.django_db
def test_get_appointments(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    Appointment.objects.create(kid=kid, doctor="Dr. Smith", date=timezone.now())
    Appointment.objects.create(kid=kid, doctor="Dr. Smith", date=timezone.now())
    Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now(), is_active=False
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "kid": kid.pk,
        "doctor": "John Doe",
        "date": (date - datetime.timedelta(days=1)).isoformat(),
        "status": "cancelled",
    }

    response = api_client.put(
        f"{reverse('appointment-detail', kwargs={'kid_pk': kid.pk, 'pk' : appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Appointment.objects.get(pk=appointment.pk).doctor == "John Doe"
    assert Appointment.objects.get(pk=appointment.pk).status == "cancelled"


@pytest.mark.django_db
def test_partial_update_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )
    data = {"score": 10, "status": "completed"}

    response = api_client.patch(
        f"{reverse('appointment-detail', kwargs={'kid_pk': kid.pk, 'pk' : appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert Appointment.objects.get(pk=appointment.pk).doctor == "Dr. Smith"
    assert Appointment.objects.get(pk=appointment.pk).status == "completed"


@pytest.mark.django_db
def test_update_other_user_appointment(api_client):
    # Checks if its possible to update an appointment to be from another user kid
    client_user = get_user_model().objects.get(username="testuser")
    client_user_kid = Kid.objects.create(
        name="John", birth_date="1990-01-01", father=client_user
    )
    appointment = Appointment.objects.create(
        kid=client_user_kid, doctor="Dr. Smith", date=timezone.now()
    )
    user = get_user_model().objects.create(
        username="testuser1", password="testpassword"
    )
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "kid": kid.pk,
        "doctor": "Dr. Smith",
        "date": date.isoformat(),
        "status": "pending",
    }

    response = api_client.put(
        f"{reverse('appointment-detail', kwargs={'kid_pk': client_user_kid.pk, 'pk' : appointment.pk})}",
        data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Kid" in response.data["detail"]


@pytest.mark.django_db
def test_delete_appointment(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    response = api_client.delete(
        f"{reverse('appointment-detail', kwargs={'kid_pk': kid.pk, 'pk' : appointment.pk})}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Appointment.objects.filter(pk=appointment.pk).exists()
    assert not Appointment.objects.get(pk=appointment.pk).is_active


@pytest.mark.django_db
def test_status_pending_score(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    data = {
        "kid": kid.pk,
        "doctor": "Dr. Smith",
        "date": date.isoformat(),
        "status": "pending",
        "score": 10,
    }

    response = api_client.post(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}", data
    )

    print(response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Score" in response.data["non_field_errors"][0]


@pytest.mark.django_db
def test_status_pending_score_partial_update(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=timezone.now()
    )

    data = {"score": 10}

    response = api_client.patch(
        f"{reverse('appointment-detail', kwargs={'kid_pk' : kid.pk, 'pk':appointment.pk})}",
        data,
    )

    print(response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Score" in response.data["non_field_errors"][0]


@pytest.mark.django_db
def test_queryset_filters_status(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="completed", score=10  # Status
    )
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=9  # Score
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?status=completed"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["status"] == "completed"


@pytest.mark.django_db
def test_queryset_filters_score(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=9  # Score
    )
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=5  # Score
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?score=9"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["score"] == appointment.score


@pytest.mark.django_db
def test_queryset_filters_score_not_int(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=9  # Score
    )
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=5  # Score
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?score=A"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Score" in response.data["detail"]


@pytest.mark.django_db
def test_queryset_filters_doctor(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = timezone.now() + datetime.timedelta(days=1)
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=date, status="cancelled", score=9  # Score
    )
    Appointment.objects.create(
        kid=kid, doctor="Dr. John", date=date, status="cancelled", score=5  # Score
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?doctor=Dr.+Smith"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["doctor"] == appointment.doctor


@pytest.mark.django_db
def test_queryset_filters_date(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = "2023-03-19 17:52:32.245014+00:00"
    appointment = Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=date, status="cancelled", score=9  # Score
    )
    Appointment.objects.create(
        kid=kid,
        doctor="Dr. John",
        date=timezone.now(),
        status="cancelled",
        score=5,  # Score
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?date=2023-03-19"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["doctor"] == appointment.doctor


@pytest.mark.django_db
def test_queryset_filters_multiple(api_client):
    user = get_user_model().objects.get(username="testuser")
    kid = Kid.objects.create(name="John", birth_date="1990-01-01", father=user)
    date = "2023-03-19 17:52:32.245014+00:00"
    Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=date, status="pending", score=10  # Status
    )
    Appointment.objects.create(
        kid=kid, doctor="Dr. Smith", date=date, status="cancelled", score=9  # Score
    )
    Appointment.objects.create(
        kid=kid,
        doctor="Dr. John",
        date=date,
        status="completed",
        score=6,  # Doctor + Date + Score + Status
    )

    response = api_client.get(
        f"{reverse('appointment-list', kwargs={'kid_pk' : kid.pk})}?status=completed&doctor=Dr.+John&score=6&date=2023-03-19"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["status"] == "completed"
    assert response.data[0]["doctor"] == "Dr. John"
