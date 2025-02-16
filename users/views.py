# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer
from users.services import send_password_reset_email, create_new_password
from users.permissions import IsTheUser, IsAdmin


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsTheUser | IsAdmin)


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsTheUser | IsAdmin)


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)


class EmailPasswordReset(APIView):
    """ View for sending email to change password """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        if user:
            response = send_password_reset_email(email)
            return Response({"message": response})
        else:
            return Response({"message": f"User with email {email} was not found"})


class PasswordReset(APIView):
    serializer = ResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, pk, token):
        user = User.objects.get(pk=pk)
        verify_user = default_token_generator.check_token(user, token)
        new_password = request.data["new_password"]
        if verify_user is True:
            response = create_new_password(user, new_password)
            return Response({"message": response})
        else:
            return Response({"message": "Something went wrong. Try again or contact admin for more information"})
