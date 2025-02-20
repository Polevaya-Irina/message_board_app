import pytest
from django.urls import reverse
from rest_framework import status

from message_board.models import Comment


@pytest.mark.django_db
def test_comment_create(api_client, ad_fixture, user_fixture):
    """Test for creating new comment"""

    url = reverse("message_board:comment_create")
    data = {"text": "Test text", "ad": ad_fixture.pk}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == "Test text"
    assert Comment.objects.count() == 1
    assert Comment.objects.first().author == user_fixture


@pytest.mark.django_db
def test_comment_update(
    api_client, comment_fixture, user_fixture, user_isowner_fixture, admin_fixture
):
    """Tests for updating comment"""

    url = reverse("message_board:comment_update", kwargs={"pk": comment_fixture.pk})
    data = {"text": "New test text"}

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "New test text"

    api_client.force_authenticate(admin_fixture)
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "New test text"


@pytest.mark.django_db
def test_comment_delete(
    api_client,
    comment_fixture,
    comment1_fixture,
    user_fixture,
    user_isowner_fixture,
    admin_fixture,
):
    """Tests for deleting comment"""

    url = reverse("message_board:comment_delete", kwargs={"pk": comment_fixture.pk})
    url1 = reverse("message_board:comment_delete", kwargs={"pk": comment1_fixture.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_isowner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 1

    api_client.force_authenticate(admin_fixture)
    response = api_client.delete(url1)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0
