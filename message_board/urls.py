from django.urls import path

from message_board.apps import MessageBoardConfig
from message_board.views import (
    AdCommentListAPIView,
    AdCreateAPIView,
    AdDestroyAPIView,
    AdListAPIView,
    AdRetrieveAPIView,
    AdUpdateAPIView,
    CommentCreateAPIView,
    CommentDestroyAPIView,
    CommentListAPIView,
    CommentUpdateAPIView,
)

app_name = MessageBoardConfig.name

urlpatterns = [
    path("ads/", AdListAPIView.as_view(), name="ad_list"),
    path("ad/<int:pk>/", AdRetrieveAPIView.as_view(), name="ad_detail"),
    path("ad/create/", AdCreateAPIView.as_view(), name="ad_create"),
    path("ad/<int:pk>/delete/", AdDestroyAPIView.as_view(), name="ad_delete"),
    path("ad/<int:pk>/update/", AdUpdateAPIView.as_view(), name="ad_update"),
    path(
        "ad/<int:pk>/comments/", AdCommentListAPIView.as_view(), name="ad_comment_list"
    ),
    path("comments/", CommentListAPIView.as_view(), name="comment_list"),
    path("comment/create/", CommentCreateAPIView.as_view(), name="comment_create"),
    path(
        "comment/<int:pk>/delete/",
        CommentDestroyAPIView.as_view(),
        name="comment_delete",
    ),
    path(
        "comment/<int:pk>/update/",
        CommentUpdateAPIView.as_view(),
        name="comment_update",
    ),
]
