from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('PF', 'PF'),
        ('PJ', 'PJ'),
    )
    user = models.OneToOneField(
        User,
        unique=True,
        on_delete=models.PROTECT,
        related_name='user_profile',
    )
    account_type = models.CharField(
        max_length=2,
        choices=ACCOUNT_TYPE_CHOICES,
        default='PF',
        verbose_name='Tipo de conta',
    )
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    cpf_cnpj = models.CharField(max_length=14, verbose_name='CPF/CNPJ')

    def __str__(self):
        return f'{self.user.username} - {self.cpf_cnpj}'

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_adress'
    )
    street = models.CharField(max_length=255, verbose_name='Rua')
    number = models.IntegerField(verbose_name='Número')
    complement = models.CharField(
        max_length=255, verbose_name='Complemento', blank=True, null=True
    )
    neighborhood = models.CharField(max_length=255, verbose_name='Bairro')
    city = models.CharField(max_length=255, verbose_name='Cidade')
    state = models.CharField(max_length=2, verbose_name='Estado')
    country = models.CharField(max_length=255, verbose_name='País')
    zip_code = models.CharField(max_length=8, verbose_name='CEP')

    def __str__(self):
        return f'{self.street}, {self.number}, {self.city}, {self.state}'

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
