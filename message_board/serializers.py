from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from message_board.models import Ad, Comment
# from message_board.validators import validate_source



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class AdSerializer(ModelSerializer):
    comment_list = SerializerMethodField(source="comment_set", read_only=True)
    # link = serializers.CharField(validators=[validate_source])

    def get_comment_list(self, ad):
        comments = Comment.objects.filter(ad=ad)
        return [comment.id for comment in comments]

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "price",
            "created_at",
            "author",
            "comment_list",
        )
