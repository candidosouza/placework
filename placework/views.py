from hmac import new
from math import e
from re import U
from typing import Any
import uuid
from django import http
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib import messages
from placework.models import EmailActivation, PasswordResetCode, Profile, Address, PasswordHistory
from placework.forms import (
    AddressForm,
    LoginForm,
    UpdateForm,
    RegisterForm,
    PasswordResetForm,
    PasswordResetConfirmForm
)
from placework.utils import (
    generate_password,
    generate_reset_code,
    is_reset_code_valid,
    send_reset_code_email,
    send_password_email,
    hash_password,
    change_password,
    send_register_code_email
)



class HomeView(TemplateView):
    template_name = 'placework/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context


class LoginView(TemplateView):
    template_name = 'placework/login.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.form = LoginForm(request.POST)

        if not self.form.is_valid():
            for field, errors in self.form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return self.handle_auth_failure(request, 'Email ou senha inválidos.')
        
        username = self.form.cleaned_data['username']
        password = self.form.cleaned_data['password']

        # Verifique se o usuário existe
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            user_profile = Profile.objects.get(user__username=username)

            if user_profile.is_blocked:
                # Usuário bloqueado por muitas tentativas incorretas
                return self.handle_auth_failure(
                    request,
                    'Usuário bloqueado! Você errou a senha 5 vezes. '
                    'Clique em "Esqueceu senha" para recuperar.'
                )
            
            if user_profile.reset_password:
                messages.error(
                    request,
                    'Você precisa redefinir sua senha.'
                )
                login(request, user)
                return redirect('password_new')
            
            if EmailActivation.objects.filter(user=user).exists():
                messages.error(
                    request,
                    'Seu email não está verificado. Acesse o link enviado para seu email.'
                )
                response = redirect('login')
                response['Location'] += '?error_active=1'
                return response

            if user is not None:
                # Senha correta, faça login e redefina as tentativas incorretas
                login(request, user)
                user_profile.error_login = 0
                user_profile.save()
                
                return redirect('home')
            else:
                # Senha incorreta, registra a tentativa e, se necessário, bloqueia o usuário
                user_profile.error_login += 1
                user_profile.save()
                
                if user_profile.error_login == 5:
                    user_profile.is_blocked = True
                    user_profile.save()
                
                remaining_attempts = 5 - user_profile.error_login
                return self.handle_auth_failure(
                    request,
                    f'Senha incorreta! Você tem mais {remaining_attempts} tentativas.'
                )
        
        # Usuário não encontrado
        return self.handle_auth_failure(
            request,
            'Usuário não localizado. Você pode se cadastrar ou fazer o login com um email registrado.'
        )

    def handle_auth_failure(self, request, error_message):
        messages.error(request, error_message)
        context = {'form': self.form}
        return render(request, 'placework/login.html', context)


class RegisterUserView(TemplateView):
    template_name = 'placework/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['name'] or form.cleaned_data['company_name']
            cpf = form.cleaned_data['cpf']
            cnpj = form.cleaned_data['cnpj']
            account_type = form.cleaned_data['account_type']
            street = form.cleaned_data['street']
            number = form.cleaned_data['number']
            complement = form.cleaned_data['complement']
            neighborhood = form.cleaned_data['neighborhood']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']


            user_exists = self.user_exists(username)
            if user_exists:
                messages.error(request, 'Email já cadastrado.')
                context = {'form': form}
                return render(request, 'placework/register.html', context)
            
            cpf_exists = self.cpf_exists(cpf)
            if cpf_exists:
                messages.error(request, 'CPF Já casdastrado.')
                context = {'form': form}
                return render(request, 'placework/register.html', context)
            
            cnpj_exists = self.cnpj_exists(cnpj)
            if cnpj_exists:
                messages.error(request, 'CNPJ Já casdastrado.')
                context = {'form': form}
                return render(request, 'placework/register.html', context)

            user = User.objects.create_user(username=username, password=password)
            user.email = username
            user.save()

            # Adicione a nova senha ao histórico
            password_history = hash_password(password)
            PasswordHistory.objects.create(
                user=user,
                hashed_password=password_history
            )

            if full_name:
                first_name, _, last_name = full_name.partition(' ')
                user.first_name = first_name
                user.last_name = last_name

            user_profile = Profile.objects.create(
                user=user, 
                account_type=account_type
            )

            if user_profile.account_type == 'PJ':
                user_profile.company_name = full_name
                user_profile.cnpj = cnpj
            if user_profile.account_type == 'PF':
                user_profile.cpf = cpf

            user_profile.save()
            user.save()

            address = Address.objects.create(
                user=user, street=street, number=number, complement=complement,
                neighborhood=neighborhood, city=city, state=state, zip_code=zip_code
            )
            address.save()

            activation = EmailActivation(user=user)
            activation.save()
            send_register_code_email(request, user, activation.token)
            messages.success(request, 'Enviamos um email com um link de ativação para o seu endereço de e-mail. Por favor, verifique sua caixa de entrada.')
            return redirect('home')

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, error)
            context = {'form': form, 'no_user': True}
            return render(request, 'placework/register.html', context)
    
    def user_exists(self, username):
        return bool(
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=username).exists()
        )
    
    def cpf_exists(self, cpf):
        return bool(
            Profile.objects.filter(cpf=cpf).exists()
        )
    
    def cnpj_exists(self, cnpj):
        return bool(
            Profile.objects.filter(cnpj=cnpj).exists()
        )


class UpdateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'placework/update.html'
    success_message = "Os dados foram atualizados com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UpdateForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(username=request.user.username).first()
            if not user:
                return redirect('home')

            password = form.cleaned_data['password']
            full_name = form.cleaned_data['name']
            if full_name:
                name_parts = full_name.split(' ', 1) 
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                user.first_name = first_name
                user.last_name = last_name
                if user.user_profile.account_type == 'PJ':
                    user.user_profile.company_name = full_name
                    user.user_profile.save()
                user.save()
            if password:
                if not change_password(user, password):
                    messages.error(request, 'A nova senha não pode corresponder a uma senha anterior.')
                    context = {'form': form}
                    return render(request, 'placework/update.html', context)
                login(request, user)
            messages.success(self.request, 'Dados Alterados com Sucesso!')
            return redirect('home')

        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, error)

        context = {'form': form}
        return render(request, 'placework/update.html', context)


class AddAddressView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'placework/add_address.html'
    form_class = AddressForm
    success_url = reverse_lazy('home')
    success_message = "Endereço adicionado com sucesso"

    def form_valid(self, form):
        with transaction.atomic():
            address = form.save(commit=False)
            address.user = self.request.user
            address.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return self.render_to_response(
            self.get_context_data(form=form)
        )

class CustomPasswordResetConfirmView(TemplateView):
    template_name = 'placework/password_reset_confirm.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('uuid')
        try:
            uuid.UUID(code)
        except ValueError:
            messages.error(request, 'Código inválido.')
            return redirect('home')
        verify_code = PasswordResetCode.objects.filter(code=code).first()
        if not verify_code:
            messages.error(request, 'Código inválido.')
            return redirect('home')
        
        if is_reset_code_valid(verify_code):
            messages.error(request, 'Código expirado.')
            # verify_code.delete()
            return redirect('home')
        
        new_password = generate_password()
        user = verify_code.user
        user.set_password(new_password)
        user.save()
        user.user_profile.error_login = 0
        user.user_profile.is_blocked = False
        user.user_profile.reset_password = True
        user.user_profile.save()

        send_password_email(user, new_password)

        verify_code.delete()

        messages.success(request, 'Senha alterada com sucesso. Enviamos no seu e-mail.')
        return redirect('login')


class NewPasswordVew(TemplateView):
    template_name = 'placework/password_new.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordResetConfirmForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            user.set_password(password)
            user.save()
            user.user_profile.reset_password = False
            user.user_profile.save()
            login(request, user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            context = {'form': form}
            return render(request, 'placework/password_new.html', context)
        


def custom_logout(request):
    logout(request)
    return redirect('home')


class PasswordResetView(View):
    template_name = 'placework/password_reset.html'

    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Não há usuário cadastrado com este e-mail.')
                return redirect('password_reset')

            code = generate_reset_code(user)
            if not send_reset_code_email(request, user, code):
                messages.error(request, 'Não foi possível enviar o e-mail de recuperação de senha.')
                return redirect('password_reset')

            messages.success(request, 'Um e-mail com instruções de recuperação de senha foi enviado para o seu endereço de e-mail.')
            return render(request, self.template_name, {'form': form})

        messages.error(request, 'Ocorreu um erro ao enviar o e-mail de recuperação de senha.')
        return redirect('password_reset')

# TODO REFATORAR VIEW DE REDEFINIÇÃO DE SENHA
# def password_reset(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             user = User.objects.filter(email=email).first()
#             if user:
#                 code = generate_reset_code(user)
#                 send_email = send_reset_code_email(request, user, code)
#                 if not send_email:
#                     messages.error(request, 'e-mail não enviado')
#                     return render(request, 'placework/password_reset.html', {'form': form})
#             else:
#                 messages.error(request, 'Não há usuário cadastrado com este e-mail.')
#                 return redirect('password_reset')   
#             messages.success(request, 'Um e-mail com instruções de recuperação de senha foi enviado para o seu endereço de e-mail.')
#             return render(request, 'placework/password_reset.html', {'form': form})
#         else:
#             messages.error(request, 'Ocorreu um erro ao enviar o e-mail de recuperação de senha.')
#             return redirect('password_reset')
#     else:
#         form = PasswordResetForm()
#     return render(request, 'placework/password_reset.html', {'form': form})


def active_email(request, email, uuid):
    activation = EmailActivation.objects.filter(token=uuid, user__email=email).first()
    if not activation:
        messages.error(request, 'Código inválido.')
        return redirect('home')
    user = activation.user
    user.user_profile.is_active = True
    user.user_profile.save()
    activation.delete()
    messages.success(request, 'E-mail verificado com sucesso. Faça o login para acessar sua conta.')
    return redirect('login')


class SedingEmailActivationView(TemplateView):
    template_name = 'placework/register_email_activation.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordResetForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, 'Não há usuário cadastrado com este e-mail.')
                return redirect('register_email_activation')
            if user.user_profile.is_active:
                messages.error(request, 'E-mail já ativado.')
                return redirect('register_email_activation')
            last_email_activate =  EmailActivation.objects.filter(user=user).first()
            if last_email_activate:
                last_email_activate.delete()
                
            activation = EmailActivation(user=user)
            activation.save()
            send_register_code_email(request, user, activation.token)
            messages.success(request, 'Reenviamos um email com um link de ativação para o seu endereço de e-mail. Por favor, verifique sua caixa de entrada.')
            return redirect('login')
        return render(request, 'placework/register_email_activation.html')
