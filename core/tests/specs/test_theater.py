import pytest

from core.tests.fixtures import user_bob, user_company


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
