from django.test import TestCase

# Create your tests here.
import random
import string
from faker import Faker
from django.contrib.auth.models import User
from.models import Profile
from django.core.exceptions import ObjectDoesNotExist

# Generate a random username
def generate_username():
    letters = string.ascii_letters
    username = ''.join(random.choice(letters) for _ in range(8))
    return username

# Generate a random password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(10))
    return password

# Create 10,000 user accounts
fake = Faker()

# ...

def create_users():
    for _ in range(10000):
        username = generate_username()
        password = generate_password()
        email = f'{username}@example.com'
        user = User.objects.create_user(username=username, password=password, email=email)
        
        phone = fake.phone_number()
        country = fake.country()
        
        # Check if a profile already exists for the user
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            # Create a profile only if it doesn't exist
            profile = Profile(user=user, phone=phone, country=country)
            profile.save()
# Run the function to create users
create_users()
