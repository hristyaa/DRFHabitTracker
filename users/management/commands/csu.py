from django.core.management import BaseCommand

from users.models import User

# from django.utils import timezone
# from datetime import timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@mail.ru")
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password("1234")
        user.save()

    # def handle(self, *args, **options):
    #     user = User.objects.create(email="test@mail.ru")
    #     user.is_active = True
    #     user.is_superuser = False
    #     user.is_staff = False
    #     user.set_password("1234")
    #     user.save()
