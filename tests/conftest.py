import pytest
from rest_framework.test import APIClient

from users.models import User
from message_board.models import Ad, Comment


@pytest.fixture
def admin_fixture():
    """ Fixture for User model - admin """
    admin = User.objects.create(
        email="admin@test.ru", password="admin", role="Администратор"
    )
    return admin


@pytest.fixture
def user_fixture():
    """ Fixture for User model - user """
    user = User.objects.create(
        email="user@test.ru", password="user", role="Пользователь"
    )
    return user


@pytest.fixture
def user_isowner_fixture():
    """ Fixture for User model - user who has created the profile or ads/comments """
    user = User.objects.create(
        email="user1@test.ru", password="user1", role="Пользователь"
    )
    return user


@pytest.fixture
def api_client():
    """ Client for testing API """
    return APIClient()


@pytest.fixture
def ad_fixture(user_isowner_fixture):
    """ Fixture for Ad model """
    ad = Ad.objects.create(
        title="Cup", description="White cup", author=user_isowner_fixture, price=100
    )
    return ad


@pytest.fixture
def ad1_fixture(user_isowner_fixture):
    """ Second fixture for Ad model, for test_ad_delete """
    ad = Ad.objects.create(
        title="Plate", description="Blue", author=user_isowner_fixture, price=200
    )
    return ad


@pytest.fixture
def comment_fixture(ad_fixture, user_isowner_fixture):
    """ Fixture for Comment model """
    comment = Comment.objects.create(
        text="Nice cup",
        author=user_isowner_fixture,
        ad=ad_fixture,
    )
    return comment


@pytest.fixture
def comment1_fixture(ad_fixture, user_isowner_fixture):
    """ Second fixture for Comment model, for test_comment_delete """
    comment = Comment.objects.create(
        text="Nice cup",
        author=user_isowner_fixture,
        ad=ad_fixture,
    )
    return comment
