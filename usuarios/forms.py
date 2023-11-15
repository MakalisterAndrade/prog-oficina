from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario

class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Usuario

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password1', 'password2', 'tipo_usuario')
