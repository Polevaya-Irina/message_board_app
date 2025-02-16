from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig

from users.views import (UserCreateAPIView, UserRetrieveAPIView, EmailPasswordReset, PasswordReset,
                         UserUpdateAPIView, UserListAPIView, UserDestroyAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("list/", UserListAPIView.as_view(), name="user_list"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("reset_password/", EmailPasswordReset.as_view(), name="password_reset"),
    path("reset_password_confirm/<int:pk>/<str:token>/", PasswordReset.as_view(), name='new_password'),
]
