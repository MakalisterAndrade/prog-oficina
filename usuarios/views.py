from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from .forms import UsuarioAuthenticationForm, UsuarioRegistroForm

class LoginView(FormView):
    template_name = 'usuarios/login.html'
    form_class = UsuarioAuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'Login bem-sucedido.')
        return redirect('clientes_list') 
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro no login. Verifique suas credenciais.')
        return super().form_invalid(form)

class RegistroView(LoginRequiredMixin, View):
    template_name = 'usuarios/registro.html'
    form_class = UsuarioRegistroForm
    success_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('clientes_list')  # Redirecione usuários autenticados para outra página se necessário
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro bem-sucedido. Faça o login para continuar.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

logout_view = DjangoLogoutView.as_view(next_page=reverse_lazy('usuarios:login'))
