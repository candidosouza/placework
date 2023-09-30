import random

from django.contrib.auth.models import User
from faker import Faker

from placework.models import Profile, Address


fake = Faker('pt_BR')

User.objects.create_superuser(
    username='admin',
    email='admin@email.com',
    password='admin',
    first_name='Admin',
    last_name='Admin',
)

for _ in range(10):
    username = fake.user_name()
    # email = fake.email()
    # user = User.objects.create_user(
    #     username=username,
    #     email=email,
    #     password='123456',
    #     first_name=fake.first_name(),
    #     last_name=fake.last_name(),
    # )

    # type_account = random.choice(['PF', 'PJ'])
    # cpf_cnpj = fake.cnpj()
    # if type_account == 'PF':
    #     cpf_cnpj = fake.cpf()
        
    # Profile.objects.create(
    #     user=user,
    #     account_type=type_account,
    #     cpf_cnpj=cpf_cnpj
    # )

    # Address.objects.create(
    #     user=user,
    #     street=fake.street_name(),
    #     number=fake.random_int(min=1, max=9999),
    #     complement=fake.street_suffix(),
    #     neighborhood=fake.bairro(),
    #     city=fake.city(),
    #     state=fake.estado_sigla(),
    #     zip_code=fake.postcode(),
    # )
