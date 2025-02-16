from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER, HOST_URL
from users.models import User
from secrets import token_bytes


def send_password_reset_email(user_email):
    """Sends email to reset the password """
    user = User.objects.filter(email=user_email).first()
    if user.is_active:
        token = default_token_generator.make_token(user)
        url = HOST_URL
        message = (f"Для восстановления доступа к аккаунту перейдите по ссылке: {url}/users/reset_password_confirm/{user.id}/{token}")
        send_mail("Восстановление доступа к аккаунту", message, EMAIL_HOST_USER, [user_email])
        return f"Password reset email was sent to {user_email}."
    else:
        return f"User with email {user_email} is inactive. Please contact the admin."

def create_new_password(user, new_password):
    """ Saves new password using user_id"""

    if user.is_active:
        user.set_password(new_password)
        user.save()
        return "Your password was changed"
    else:
        return f"User with email {user.email} is inactive. Please contact the admin."
