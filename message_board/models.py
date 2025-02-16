from django.db import models

from config import settings


class Ad(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название товара",
        help_text="Введите название товара",
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Введите описание товара",
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Время и дата создания объявления",
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена товара",
        help_text="Укажите цену товара",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Автор",
        help_text="Укажите автора объявления",
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"Товар {self.id} {self.title}"


class Comment(models.Model):
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name="Текст отзыва",
        help_text="Введите текст отзыва",
    )
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, verbose_name="Объявление"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Автор комментария",
        help_text="Укажите автора комментария",
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Время и дата создания объявления",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.id} к объявлению {self.ad}"
