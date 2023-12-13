from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from accounts.models import Profile
from faker import Faker
from PIL import Image
import os
import sqlite3

def create_users_with_images(num_users):
    fake = Faker()

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        phone = fake.phone_number()
        slug = slugify(username)

        try:
            user = User.objects.create(username=username, email=email)
        except sqlite3.IntegrityError:
            print(f"Skipping creation for username: {username}")
            continue

        profile, created = Profile.objects.get_or_create(user=user)

        if created:
            profile.phone = phone
            profile.slug = slug
            profile.save()

        print(f"User created: {username}")


# Usage
create_users_with_images(1000000)  # Pass the number of users you want to create
