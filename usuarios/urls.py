from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CadastroView, meu_perfil

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('perfil/', meu_perfil, name='perfil'),
]