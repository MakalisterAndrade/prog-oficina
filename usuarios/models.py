from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('balconista', 'Balconista'),
        ('administrador', 'Administrador'),
    )

    username = models.CharField(max_length=50, unique=True)
    tipo_usuario = models.CharField(max_length=15, choices=TIPOS_USUARIO, default='balconista')
