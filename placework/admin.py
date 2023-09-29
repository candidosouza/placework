from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from placework.models import Address, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, AddressInline)
    list_display = ('name', 'email', 'accout_type', 'cpf_cnpj')
    list_display_links = (
        'name',
        'email',
    )
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'user_profile__cpf_cnpj',
    )
    list_filter = (
        'user_profile__account_type',
        'user_profile__is_active',
    )

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def accout_type(self, obj):
        return obj.user_profile.account_type

    def cpf_cnpj(self, obj):
        return obj.user_profile.cpf_cnpj

    name.short_description = 'Nome'
    accout_type.short_description = 'Tipo de conta'
    cpf_cnpj.short_description = 'CPF/CNPJ'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
