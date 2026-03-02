from django.test import Client
import pytest

from core import models

@pytest.fixture
def user_bob(db):
    user = models.User.objects.create_user(
        username="bob",
        email="bob@exampel.com",
        password="I_am_Bob",
    )
    user.save()

    book_user = models.BookUser(
        user=user,
    )
    book_user.save()

    auth_client = Client()
    auth_client.force_login(user)

    book_user.client = auth_client

    return book_user


@pytest.fixture
def user_company(db):
    user = models.User.objects.create_user(
        username="UGC",
        email="ugc@ugc.com",
        password="I_am_Bob",
    )
    user.save()

    book_user = models.BookUser(
        user=user,
        is_company=True,
    )
    book_user.save()

    auth_client = Client()
    auth_client.force_login(user)

    book_user.client = auth_client

    return book_user


# fixture locale: cree une salle appartenant a  user_company
@pytest.fixture
def theater_ugc(user_company, db):
    theater = models.Theater(
        name="UGC Ciné Cité Paris",
        address="30 Pl. de la République, 75011 Paris",
        owner=user_company,
        provider="ugc",
    )
    
    theater.save()
    return theater


# Fiture locale, un deuxième company user (non propriétaire de la salle UGC)
@pytest.fixture
def user_company2(db):
    from django.test import Client
    user = models.User.objects.create_user(
        username="MK2",
        email="mk2@mk2.com",
        password="I_am_MK2",
    )
    user.save()
    
    book_user = models.BookUser(user=user, is_company=True)
    book_user.save()
    
    auth_client = Client()
    auth_client.force_login(user)
    book_user.client = auth_client
    return book_user

