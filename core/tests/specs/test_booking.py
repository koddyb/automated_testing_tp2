import pytest
from unittest.mock import patch

from core.tests.fixtures import user_bob, user_company
from core import models

#--------------------Fixtures pour les test des reservations
@pytest.fixture
def theater_mk2(user_company, db):
    theater = models.Theater.objects.create(
        name="MK2 Gambetta",
        address="6 Av. du Père Lachaise, 75020 Paris",
        owner=user_company,
        provider="mk2",
    )
    return theater


@pytest.fixture
def theater_ugc(user_company, db):
    theater = models.Theater.objects.create(
        name="UGC Ciné Cité Paris",
        address="30 Pl. de la République, 75011 Paris",
        owner=user_company,
        provider="ugc",
    )
    return theater


@pytest.fixture
def theater_gaumont(user_company, db):
    theater = models.Theater.objects.create(
        name="Gaumont Opéra",
        address="2 Bd des Capucines, 75009 Paris",
        owner=user_company,
        provider="gaumont",
    )
    return theater
#--------------------Fixtures pour les test des reservations




@pytest.mark.django_db
@patch("external_apis.mk2.book_seat")
def test_book_mk2(mock_book_seat, user_bob, theater_mk2):
    # Given
    mock_book_seat.return_value = {"success": True}
    payload = {
        "theater_id": theater_mk2.id,
        "movie_name": "Inception",
        "date": "2026-12-31 20:00:00",
    }

    # When
    response = user_bob.client.post("/core/book_movie/", payload, content_type="application/json")

    # Then
    assert response.status_code == 200
    mock_book_seat.assert_called_once_with(
        theater_name="MK2 Gambetta",
        movie_name="Inception",
        date="2026-12-31 20:00:00",
    )


@pytest.mark.django_db
@patch("external_apis.ugc.reserve")
def test_book_ugc(mock_reserve, user_bob, theater_ugc):
    # Given
    mock_reserve.return_value = {"success": True}
    payload = {
        "theater_id": theater_ugc.id,
        "movie_name": "Inception",
        "date": "2026-12-31 20:00:00",
    }

    # When
    response = user_bob.client.post("/core/book_movie/", payload, content_type="application/json")

    # Then
    assert response.status_code == 200
    mock_reserve.assert_called_once_with(
        film="Inception",
        salle="UGC Ciné Cité Paris",
        horaire="2026-12-31 20:00:00",
    )


@pytest.mark.django_db
@patch("external_apis.gaumont.make_reservation")
def test_book_gaumont(mock_make_reservation, user_bob, theater_gaumont):
    # Given
    mock_make_reservation.return_value = {"success": True}
    payload = {
        "theater_id": theater_gaumont.id,
        "movie_name": "Inception",
        "date": "2026-12-31 20:00:00",
    }

    # When
    response = user_bob.client.post("/core/book_movie/", payload, content_type="application/json")

    # Then
    assert response.status_code == 200
    mock_make_reservation.assert_called_once_with({
        "movie": "Inception",
        "theater": "Gaumont Opéra",
        "when": "2026-12-31 20:00:00",
    })


@pytest.mark.django_db
def test_book_unauthenticated(client, theater_mk2):
    # Given : client non authentifié
    payload = {
        "theater_id": theater_mk2.id,
        "movie_name": "Inception",
        "date": "2026-12-31 20:00:00",
    }

    # When
    response = client.post("/core/book_movie/", payload, content_type="application/json")

    # Then
    assert response.status_code == 403

