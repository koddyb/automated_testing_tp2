import pytest

from core.tests.fixtures import user_bob, user_company, theater_ugc, user_company2
from core import models

@pytest.mark.django_db
def test_create_theater(user_company):
    # Given
    theater_payload = {
        "name": "UGC Cinecité Paris",
        "address": "30 Place de la République 75011 Paris",
    }

    # When
    response = user_company.client.post(
        "/core/theater/create/",
        theater_payload,
        content_type="application/json",
    )

    # Then
    assert response.status_code == 201
    created_theater = response.json()

    assert created_theater["name"] == "UGC Cinecité Paris"
    assert created_theater["address"] == "30 Place de la République 75011 Paris"
    assert created_theater["id"] is not None


@pytest.mark.django_db
def test_create_theater__not_company(user_bob):
    # Given
    theater_payload = {
        "name": "Téatre Bidon",
        "address": "Adresse Bidon",
    }

    # When
    response = user_bob.client.post(
        "/core/theater/create/",
        theater_payload,
        content_type="application/json",
    )

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_screening(user_company, theater_ugc):
    # Given
    screening_payload = {
        "theater_id": theater_ugc.id,
        "movie_name": "Inception",
        "date": "2026-12-31T20:00:00",
    }

    # When
    response = user_company.client.post(
        "/core/theater/screening/add/",
        screening_payload,
        content_type="application/json",
    )

    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["movie_name"] == "Inception"
    assert data["theater_id"] == theater_ugc.id
    assert data["id"] is not None


@pytest.mark.django_db
def test_cancel_screening(user_company, theater_ugc):
    # Given : créer une séance d'abord
    screening = models.Screening(
        movie_name="Inception",
        date="2026-12-31 20:00:00",
        theater=theater_ugc,
    )
    screening.save()

    # When
    response = user_company.client.delete(
        "/core/theater/screening/cancel/",
        {"screening_id": screening.id},
        content_type="application/json",
    )

    # Then
    assert response.status_code == 204
    assert not models.Screening.objects.filter(pk=screening.id).exists()


@pytest.mark.django_db
def test_cancel_screening__not_owner(user_company2, theater_ugc):
    # Given : séance appartenant à UGC, tentative par MK2
    screening = models.Screening(
        movie_name="Inception",
        date="2026-12-31 20:00:00",
        theater=theater_ugc,
    )
    screening.save()

    # When
    response = user_company2.client.delete(
        "/core/theater/screening/cancel/",
        {"screening_id": screening.id},
        content_type="application/json",
    )

    # Then
    assert response.status_code == 403
    # La séance n'a pas été supprimée
    assert models.Screening.objects.filter(pk=screening.id).exists()

