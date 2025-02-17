from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from message_board.models import Ad, Comment
from message_board.pagination import AdPagination, CommentPagination
from message_board.serializers import AdSerializer, CommentSerializer
from users.permissions import IsAdmin, IsOwner


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class AdListAPIView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (AllowAny,)
    pagination_class = AdPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    search_fields = ["title", "description"]


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)


class AdUpdateAPIView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsAdmin)


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsAdmin)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        comment = serializer.save()
        comment.author = self.request.user
        comment.save()


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination


class AdCommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        ad_id = self.kwargs.get("pk")
        queryset = self.queryset.filter(ad=ad_id)
        return queryset


class CommentUpdateAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsAdmin)


class CommentDestroyAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsAdmin)
