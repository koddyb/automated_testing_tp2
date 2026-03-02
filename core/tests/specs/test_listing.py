import pytest

from core.tests.fixtures import user_company, theater_ugc, theater_mk2
from core import models

@pytest.mark.django_db
def test_list_movies(client, theater_mk2, theater_ugc):
    # Given : 2 films differents dans 2 salles
    models.Screening.objects.create(movie_name="Inception", date="2026-12-31T20:00:00+00:00", theater=theater_mk2)
    models.Screening.objects.create(movie_name="Dune", date="2026-12-31T22:00:00+00:00", theater=theater_ugc)

    # When
    response = client.get("/core/movies/")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(data["movies"]) == {"Inception", "Dune"}


@pytest.mark.django_db
def test_list_movies__deduplication(client, theater_mk2, theater_ugc):
    # Given : le meme film dans 2 salles ne doit apparaître qu'une fois
    models.Screening.objects.create(movie_name="Inception", date="2026-12-31T20:00:00+00:00", theater=theater_mk2)
    models.Screening.objects.create(movie_name="Inception", date="2026-12-31T22:00:00+00:00", theater=theater_ugc)

    # When
    response = client.get("/core/movies/")

    # Then
    assert response.status_code == 200
    assert response.json()["movies"] == ["Inception"]


@pytest.mark.django_db
def test_list_screenings_for_movie(client, theater_mk2, theater_ugc):
    # Given : une meme film dans 2 salles 
    models.Screening.objects.create(movie_name="Inception", date="2026-12-31T20:00:00+00:00", theater=theater_mk2)
    models.Screening.objects.create(movie_name="Inception", date="2026-12-31T22:00:00+00:00", theater=theater_ugc)
    
    #un autre film
    #models.Screening.objects.create(movie_name="Dune", date="2026-12-31T18:00:00+00:00", theater=theater_mk2)

    # When
    response = client.get("/core/movies/screenings/?movie=Inception")

    # Then
    assert response.status_code == 200
    screenings = response.json()["screenings"]
    assert len(screenings) == 2
    theater_names = {s["theater_name"] for s in screenings}
    assert theater_names == {"MK2 Gambetta", "UGC Ciné Cité Paris"}


@pytest.mark.django_db
def test_list_screenings__missing_param(client):
    # When : pas de query param ?movie=
    response = client.get("/core/movies/screenings/")

    # Then
    assert response.status_code == 400
