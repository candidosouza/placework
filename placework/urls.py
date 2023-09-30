from django.urls import path
from placework.views import (
    HomeView,
    LoginView,
    RegisterUserView,
    UpdateView,
    AddAddressView,
    custom_logout
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cadastro/', RegisterUserView.as_view(), name='register'),
    path('alteracao-dados/<int:pk>/', UpdateView.as_view(), name='update'),
    path('adicionar-endereco/<int:pk>/', AddAddressView.as_view(), name='add_address'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]