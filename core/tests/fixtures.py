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
