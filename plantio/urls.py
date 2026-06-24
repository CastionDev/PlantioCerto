from django.urls import path
from . import views

urlpatterns = [
    path('recomendacao/', views.recomendacao_por_cep, name='recomendacao'),
    path('clima/', views.clima_atual, name='clima'),
]