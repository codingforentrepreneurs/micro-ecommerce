from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the admin superuser with username and password as admin"

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(username="admin").exists():
            print("Admin user already exists!")
            return
        print("Creating admin user ..")
        User.objects.create_superuser("admin", "admin@example.com", "admin")
        print("Creating admin user ..")
