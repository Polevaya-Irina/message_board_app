from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="mirwen@yandex.ru")
        user.set_password("mirwen")
        user.is_active = True
        user.role = "Администратор"
        user.save()
