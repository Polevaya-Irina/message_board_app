from django.contrib import admin

# Register your models here.
from django.contrib import admin

from message_board.models import Ad, Comment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "created_at", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "author", "created_at")
