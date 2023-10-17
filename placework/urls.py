from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from placework.views import (
    HomeView,
    LoginView,
    RegisterUserView,
    UpdateView,
    AddAddressView,
    CustomPasswordResetConfirmView,
    NewPasswordVew,
    SedingEmailActivationView,
    PasswordResetView,
    custom_logout,
    # password_reset,
    active_email,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cadastro/', RegisterUserView.as_view(), name='register'),
    path('cadastro/active_email/<email>/<uuid>/', active_email, name='register_active_email'),
    path('cadastro/sending_email_activation/', SedingEmailActivationView.as_view(), name='register_email_activation'),
    path('alteracao-dados/<int:pk>/', UpdateView.as_view(), name='update'),
    path('adicionar-endereco/<int:pk>/', AddAddressView.as_view(), name='add_address'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uuid>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_new/', NewPasswordVew.as_view(), name='password_new'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)