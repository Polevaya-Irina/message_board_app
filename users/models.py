import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    uid = models.UUIDField(unique=True, default=uuid.uuid4, null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True,
        help_text="Введите ваше имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
        null=True,
        help_text="Введите вашу фамилию",
    )
    image = models.ImageField(
        upload_to="photos/",
        verbose_name="Аватарка",
        help_text="Загрузите Вашу аватарку",
    )

    USER = "Пользователь"
    ADMIN = "Администратор"

    ROLE_CHOICES = [
        (USER, "User"),
        (ADMIN, "Admin"),
    ]
    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name="Роль пользователя",
        help_text="Выберите роль пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}, email: {self.email}"
