import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from rest_framework import status

from users.models import User
from users.tests.conftest import api_client, user_fixture, admin_fixture, user_isowner_fixture


@pytest.mark.django_db
def test_user_create(client):
    """ Test for creating new user"""

    url = reverse("users:register")
    data = {"email": "second_user@test.ru", "password": "second_user"}
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert response.data["email"] == "second_user@test.ru"


@pytest.mark.django_db
def test_user_list(api_client, user_fixture, admin_fixture):
    """ Tests for users list endpoint"""

    url = reverse("users:user_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)
    # print(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_user_retrieve(api_client, user_fixture, admin_fixture, user_isowner_fixture):
    """ Tests for detailed info of one user """

    url = reverse("users:user_detail", kwargs={"pk": user_isowner_fixture.pk})

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "user1@test.ru"

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "user1@test.ru"


@pytest.mark.django_db
def test_user_update(api_client, user_fixture, user_isowner_fixture, admin_fixture):
    """ Tests for updating user """

    url = reverse("users:user_update", kwargs={"pk": user_isowner_fixture.pk})
    data = {"first_name": "Testname"}

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Testname"

    api_client.force_authenticate(admin_fixture)
    response = api_client.patch(url, data)
    print(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Testname"


@pytest.mark.django_db
def test_user_delete(api_client, user_fixture, user_isowner_fixture, admin_fixture):
    """ Tests for deleting user"""

    url = reverse("users:user_delete", kwargs={"pk": user_isowner_fixture.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(admin_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_user_reset_password(user_fixture, api_client):
    """ Testing email password reset endpoint """

    url = reverse("users:password_reset")
    data = {"email": user_fixture.email}

    response = api_client.post(url, data)
    print(response)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Password reset email was sent to {user_fixture.email}."


@pytest.mark.django_db
def test_user_reset_password_confirm(user_fixture, api_client):
    """ Testing password reset endpoint """

    token = default_token_generator.make_token(user_fixture)
    url = reverse("users:new_password", kwargs={"pk": user_fixture.pk, "token": token})
    data = {
        "new_password": "NewPassword",
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Your password was changed"
