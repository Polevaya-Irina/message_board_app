import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def admin_fixture():
    """Fixture for User model - admin"""
    admin = User.objects.create(
        email="admin@test.ru", password="admin", role="Администратор"
    )
    return admin


@pytest.fixture
def user_fixture():
    """Fixture for User model - user"""
    user = User.objects.create(
        email="user@test.ru", password="user", role="Пользователь"
    )
    return user


@pytest.fixture
def user_isowner_fixture():
    """Fixture for User model - user who has created the profile or ads/comments"""
    user = User.objects.create(
        email="user1@test.ru", password="user1", role="Пользователь"
    )
    return user


@pytest.fixture
def api_client():
    """
    Клиент для тестирования API
    """
    return APIClient()
