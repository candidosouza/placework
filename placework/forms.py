import re
from typing import Any
from django import forms
from django.contrib.auth.models import User
from validate_docbr import CPF, CNPJ
from placework.models import Profile, Address


def validar_cpf(cpf):
    cpf_validator = CPF()
    if not cpf_validator.validate(cpf):
        raise forms.ValidationError('CPF inválido.')


def validar_cnpj(cnpj):
    cnpj_validator = CNPJ()
    if not cnpj_validator.validate(cnpj):
        raise forms.ValidationError('CNPJ inválido.')


class RegisterForm(forms.Form):
    username = forms.EmailField(
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'autocomplete': 'current-password'
            }
        )
    )

    account_type = forms.ChoiceField(
        label='Tipo de conta',
        choices=Profile.ACCOUNT_TYPE_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de conta'
            }
        )
    )
    name = forms.CharField(
        label='Nome',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }
        )   
    )

    company_name = forms.CharField(
        label='Nome da empresa',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa'
            }
        )
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CPF'
            }
        ),
        validators=[validar_cpf]
    )

    cnpj = forms.CharField(
        label='CNPJ',
        max_length=18,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CNPJ'
            }
        ),
        validators=[validar_cnpj]
    )

    street = forms.CharField(
        label='Rua',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rua'
            }
        )
    )

    number = forms.IntegerField(
        label='Número',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }
        )
    )

    complement = forms.CharField(
        label='Complemento',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Complemento'
            }
        )
    )

    neighborhood = forms.CharField(
        label='Bairro',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        max_length=2,
        min_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Estado'
            }
        )
    )

    zip_code = forms.CharField(
        label='CEP',
        max_length=9,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CEP'
            }
        )
    )

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'complement', 'neighborhood', 'city', 'state', 'zip_code']
    
    street = forms.CharField(
        label='Rua',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rua'
            }
        )
    )

    number = forms.IntegerField(
        label='Número',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }
        )
    )

    complement = forms.CharField(
        label='Complemento',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Complemento'
            }
        )
    )

    neighborhood = forms.CharField(
        label='Bairro',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        max_length=2,
        min_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Estado'
            }
        )
    )

    zip_code = forms.CharField(
        label='CEP',
        max_length=9,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CEP'
            }
        )
    )


class LoginForm(forms.Form):
    username = forms.EmailField(
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'autocomplete': 'current-password'
            }
        )
    )


class UpdateForm(forms.Form):
    name = forms.CharField(
        label='Alterar Nome (deixe em branco se não deseja alterar):',
        max_length=254,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }
        )
    )
    password = forms.CharField(
        label='Alterar Senha (deixe em branco se não deseja alterar):',
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'autocomplete': 'current-password'
            }
        )
    )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )

    class Meta:
        model = User


class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(
        label='Digite sua nova senha',
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nova Senha',
                'autocomplete': 'current-password'
            }
        )
    )

    class Meta:
        model = User
