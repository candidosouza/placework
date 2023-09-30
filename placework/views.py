from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib import messages
from placework.models import Profile, Address
from placework.forms import (
    AddressForm,
    LoginForm,
    UpdateForm,
    RegisterForm
)


class HomeView(TemplateView):
    template_name = 'placework/home.html'


class LoginView(TemplateView):
    template_name = 'placework/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Senha incorreta.')
                    context = {'form': form}
                    return render(request, 'placework/login.html', context)
            messages.error(request, 'Usuário não localizado. Você pode se cadastrar ou fazer o login com um email registrado.')
            context = {'form': form}
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, error)
        else:
            messages.error(request, 'Email ou senha inválidos.')
            context = {'form': form, 'no_user': True}

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

            user = authenticate(username=username, password=password)
            login(request, user)
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
                user.set_password(password)
                user.save()
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

def custom_logout(request):
    logout(request)
    return redirect('home')
