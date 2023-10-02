from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from validate_docbr import CPF, CNPJ
import uuid


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
    is_active = models.BooleanField(default=False, verbose_name='Ativo')
    company_name = models.CharField(max_length=255, verbose_name='Nome da empresa', blank=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', blank=True, null=True, unique=True)
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ', blank=True, null=True, unique=True)
    error_login = models.IntegerField(default=0, verbose_name='Erros de login')
    is_blocked = models.BooleanField(default=False, verbose_name='Bloqueado')
    reset_password = models.BooleanField(default=False, verbose_name='Redefinir senha')

    def __str__(self):
        return f'{self.user.username}'

    def clean(self):
        if self.cpf:
            cpf_validator = CPF()
            if not cpf_validator.validate(self.cpf):
                raise ValidationError({'cpf': 'CPF inválido.'})

        if self.cnpj:
            cnpj_validator = CNPJ()
            if not cnpj_validator.validate(self.cnpj):
                raise ValidationError({'cnpj': 'CNPJ inválido.'})
    
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
    zip_code = models.CharField(max_length=9, verbose_name='CEP')

    def __str__(self):
        return f'{self.street}, {self.number}, {self.city}, {self.state}'

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expiration_time = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user: {self.user.email}, token: {self.token}, expira em: {self.expiration_time}'

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reset_code')
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expiration_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user: {self.user.email}, code: {self.code}, expira em: {self.expiration_time}'


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    hashed_password = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username