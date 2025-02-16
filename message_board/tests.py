from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.fields import DateField

from message_board.models import Ad, Comment
from users.models import User


class AdTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@test.ru")
        self.ad = Ad.objects.create(
            title="Cup",
            description="White cup",
            author=self.user,
            price=100,
            # created_at=date.today()
        )
        self.client.force_authenticate(user=self.user)

    def test_ad_retrieve(self):
        url = reverse("message_board:ad_detail", args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.ad.title)

    def test_ad_create(self):
        url = reverse("message_board:ad_create")
        data = {
            "title": "Plate",
            "description": "Wooden plate",
            "price": 200,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.all().count(), 2)

    def test_ad_update(self):
        url = reverse("message_board:ad_update", args=(self.ad.pk,))
        data = {
            "title": "Cup",
            "description": "White cup",
            "price": 20,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("price"), 20)

    def test_ad_delete(self):
        url = reverse("message_board:ad_delete", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.all().count(), 0)

    def test_ad_list(self):
        url = reverse("message_board:ad_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drf_str_datetime = DateField().to_representation
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "title": "Cup",
                    "description": "White cup",
                    "price": 100,
                    "created_at": drf_str_datetime(self.ad.created_at),
                    "author": self.user.id,
                    "comment_list": []
                }
            ],
        }
        self.assertEqual(data, result)


class CommentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@test.ru")
        self.ad = Ad.objects.create(
            title="Cup",
            description="White cup",
            author=self.user,
            price=100,
            created_at=date.today(),
        )
        self.comment = Comment.objects.create(
            text="Nice cup",
            author=self.user,
            ad=self.ad,
            created_at=date.today(),
        )
        self.client.force_authenticate(user=self.user)

    def test_comment_create(self):
        url = reverse("message_board:comment_create")
        data = {
            "text": "Wonderful",
            "author": self.user.id,
            "ad": self.ad.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.all().count(), 2)

    def test_comment_update(self):
        url = reverse("message_board:comment_update", args=(self.comment.pk,))
        data = {
            "text": "Very nice cup",
            "ad": self.ad.id,
            "author": self.user.id,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "Very nice cup")

    def test_comment_delete(self):
        url = reverse("message_board:comment_delete", args=(self.comment.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_comment_list(self):
        url = reverse("message_board:comment_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        drf_str_datetime = DateField().to_representation
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "text": "Nice cup",
                    "ad": self.ad.id,
                    "created_at": drf_str_datetime(self.comment.created_at),
                    "author": self.user.id,
                }
            ],
        }
        self.assertEqual(data, result)
