import pytest
from django.urls import reverse
from rest_framework import status

from message_board.models import Ad
from users.tests.conftest import (
    admin_fixture,
    api_client,
    user_fixture,
    user_isowner_fixture,
)


@pytest.mark.django_db
def test_ad_create(api_client, user_fixture):
    """Test for creating new ad"""

    url = reverse("message_board:ad_create")
    data = {"title": "Test title", "description": "Test description", "price": 100}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test title"
    assert Ad.objects.count() == 1
    assert Ad.objects.first().author == user_fixture


@pytest.mark.django_db
def test_ad_list(api_client, ad_fixture, user_fixture, admin_fixture):
    """Tests for ads list endpoint"""

    url = reverse("message_board:ad_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1


@pytest.mark.django_db
def test_ad_retrieve(
    api_client, ad_fixture, user_fixture, admin_fixture, user_isowner_fixture
):
    """Tests for detailed info of one ad"""

    url = reverse("message_board:ad_detail", kwargs={"pk": ad_fixture.pk})

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Cup"

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Cup"

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Cup"


@pytest.mark.django_db
def test_ad_update(
    api_client, ad_fixture, user_fixture, user_isowner_fixture, admin_fixture
):
    """Tests for updating ad"""

    url = reverse("message_board:ad_update", kwargs={"pk": ad_fixture.pk})
    data = {"title": "New cup"}

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "New cup"

    api_client.force_authenticate(admin_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "New cup"


@pytest.mark.django_db
def test_ad_delete(
    api_client,
    ad_fixture,
    ad1_fixture,
    user_fixture,
    user_isowner_fixture,
    admin_fixture,
):
    """Tests for deleting ad"""

    url = reverse("message_board:ad_delete", kwargs={"pk": ad_fixture.pk})
    url1 = reverse("message_board:ad_delete", kwargs={"pk": ad1_fixture.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 1

    api_client.force_authenticate(admin_fixture)
    response = api_client.delete(url1)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def test_ad_comment_list(
    api_client,
    ad_fixture,
    comment_fixture,
    comment1_fixture,
    user_fixture,
    admin_fixture,
):
    """Tests for list of comments for one ad"""

    url = reverse("message_board:ad_comment_list", kwargs={"pk": ad_fixture.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 2

    api_client.force_authenticate(admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 2
