from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from accounts.models import Profile
from faker import Faker
from PIL import Image
import os

fake = Faker()
image_dir = "static/images/New folder"

class Command(BaseCommand):
    help = 'Create multiple users and their profiles.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created.')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        image_files = os.listdir(image_dir)

        for _ in range(total):
            username = fake.user_name()
            phone = fake.phone_number()
            country = fake.country()
            address = fake.address()

            user = User.objects.create(username=username)
            profile = Profile(user=user, phone=phone, country=country, address=address)

            image_file = fake.random_element(image_files)
            image_path = os.path.join(image_dir, image_file)
            with open(image_path, 'rb') as f:
                django_file = Image.open(f)
                profile.image.save(image_file, django_file, save=True)

            profile.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} users and their profiles.'))
