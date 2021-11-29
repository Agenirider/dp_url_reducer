from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_model = get_user_model()
        admin = user_model.objects.filter(email='admin')

        # Create admin
        if not admin.exists():
            admin_user = user_model(email='admin',
                                    username='admin',
                                    password=make_password('nimda'),
                                    first_name='Admin',
                                    last_name='Adminovich',
                                    is_superuser=True,
                                    is_staff=True)

            admin_user.save()
