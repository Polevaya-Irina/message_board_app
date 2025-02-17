import pytest

from message_board.models import Ad, Comment
from users.tests.conftest import user_isowner_fixture


@pytest.fixture
def ad_fixture(user_isowner_fixture):
    """Fixture for Ad model"""
    ad = Ad.objects.create(
        title="Cup", description="White cup", author=user_isowner_fixture, price=100
    )
    return ad


@pytest.fixture
def ad1_fixture(user_isowner_fixture):
    """Second fixture for Ad model, for test_ad_delete"""
    ad = Ad.objects.create(
        title="Plate", description="Blue", author=user_isowner_fixture, price=200
    )
    return ad


@pytest.fixture
def comment_fixture(ad_fixture, user_isowner_fixture):
    """Fixture for Comment model"""
    comment = Comment.objects.create(
        text="Nice cup",
        author=user_isowner_fixture,
        ad=ad_fixture,
    )
    return comment


@pytest.fixture
def comment1_fixture(ad_fixture, user_isowner_fixture):
    """Second fixture for Comment model, for test_comment_delete"""
    comment = Comment.objects.create(
        text="Nice cup",
        author=user_isowner_fixture,
        ad=ad_fixture,
    )
    return comment
