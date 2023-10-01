from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from placework.models import Address, Profile, PasswordResetCode


class ProfileInline(admin.StackedInline):
    model = Profile


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


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
        'user_profile__cpf',
        'user_profile__cnpj',
        'user_profile__company_name',
    )
    list_filter = (
        'user_profile__account_type',
        'user_profile__is_active',
    )

    def name(self, obj):
        if company_name := obj.user_profile.company_name:
            return company_name
        return f'{obj.first_name} {obj.last_name}'

    def accout_type(self, obj):
        return obj.user_profile.account_type

    def cpf_cnpj(self, obj):
        if obj.user_profile.account_type == 'PF':
            return obj.user_profile.cpf
        return obj.user_profile.cnpj

    name.short_description = 'Nome / Razão Social'
    accout_type.short_description = 'Tipo de conta'
    cpf_cnpj.short_description = 'CPF/CNPJ'




class PasswordResetCodeAdmin(BaseUserAdmin):
    list_display = ('email', 'code', 'created_at',)
    list_filter = (
        'created_at',
    )

    def email(self, obj):
        return self.obj.user.email


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PasswordResetCode)
