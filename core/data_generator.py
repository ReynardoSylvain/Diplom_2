from faker import Faker
import random
import string

fake_data_generator = Faker()

def create_username():
    return fake_data_generator.user_name() + str(random.randint(1, 100))

def create_email():
    return fake_data_generator.email()

def create_password(min_length=8):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for _ in range(min_length))