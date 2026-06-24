from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    cep      = models.CharField(max_length=9, blank=True)
    cidade   = models.CharField(max_length=100, blank=True)
    estado   = models.CharField(max_length=2, blank=True)
    regiao   = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username