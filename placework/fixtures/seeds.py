import random

from django.contrib.auth.models import User
from faker import Faker

from placework.models import Address, Profile

fake = Faker('pt_BR')

user = User.objects.create_superuser(
    username='admin',
    email='admin@email.com',
    password='admin',
    first_name='Admin',
    last_name='Last Name',
)

Profile.objects.create(
    user=user,
    account_type=Profile.ACCOUNT_TYPE_CHOICES[0][0],
    cpf=fake.cpf(),
)

Address.objects.create(
    user=user,
    zip_code=fake.postcode(),
    street=fake.street_name(),
    number=fake.building_number(),
    neighborhood=fake.bairro(),
    city=fake.city(),
    state=fake.estado_sigla(),
)
