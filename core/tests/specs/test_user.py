import pytest

from core.tests.fixtures import user_bob


@pytest.mark.django_db
def test_create_user(client):
    # Given
    user_payload = {
        "name": "Bob",
        "email": "bob@example.com",
	    "password": "I_am_Bob",
    }

    # When
    response = client.post(
        "/core/user/create/",
        user_payload,
        content_type="application/json",
    )
    
    # Then
    assert response.status_code == 201
    created_user = response.json()
    
    assert created_user["username"] == "Bob"
    assert created_user["email"] == "bob@example.com"
    assert created_user["id"] is not None
    
    # Verification: Is id in base
    response = client.get(
        f"/core/user/get/?id={created_user['id']}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created_user["id"],
        "username": "Bob",
        "email": "bob@example.com",
        "is_company": False,
    }
    
@pytest.mark.django_db
def test_create_user__company_case(client):
    #GIVEN
    user_payload = {
        "name": "UGC",
        "email": "ugc@ugc.com",
        "password": "I_am_Bob",
        "is_company": True,
    }
    
    #When 
    response = client.post(
        "/core/user/create/",
        user_payload,
        content_type="application/json",
    )
    created_user = response.json()
    response = client.get(
        f"/core/user/get/?id={created_user['id']}",
    )
    
    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": created_user["id"],
        "username": "UGC",
        "email": "ugc@ugc.com",
        "is_company": True
    }
    

@pytest.mark.django_db
def test_get_my_profile__authenticated(user_bob):
    # Given

    # When
    response = user_bob.client.get("/core/user/my_profile/")

    # Then
    assert response.status_code == 200
    assert response.json()["id"] == user_bob.id


@pytest.mark.django_db
def test_get_my_profile__unauthenticated(client):
    # Given

    # When
    response = client.get("/core/user/my_profile/")

    # Then
    assert response.status_code == 403
