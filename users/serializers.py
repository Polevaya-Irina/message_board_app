from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    """ Serializer for User model for CRUD """
    # inner_id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class ResetPasswordSerializer(serializers.Serializer):
    """ Serializer for sending email to change password """

    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """ Serializer for changing password """

    # user_id = serializers.IntegerField(required=True)
    # token = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=8, required=True)
