from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.models import Group
from django.views.generic import TemplateView

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

class RegistroView(View):
    template_name = 'usuarios/registro.html'
    form_class = UsuarioRegistroForm
    success_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        user_role = request.user.tipo_usuario if request.user.is_authenticated else None
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'user_role': user_role})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()


            tipo_usuario = form.cleaned_data.get('tipo_usuario')
            user_role = tipo_usuario  # Defina user_role diretamente com tipo_usuario

            try:
                group, created = Group.objects.get_or_create(name=tipo_usuario)
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, 'Group does not exist for tipo_usuario: {}'.format(tipo_usuario))
            except Exception as e:
                messages.error(request, 'An error occurred: {}'.format(str(e)))

            messages.success(request, 'Registro bem-sucedido. Faça o login para continuar.')
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'user_role': request.user.tipo_usuario})


logout_view = DjangoLogoutView.as_view(next_page=reverse_lazy('usuarios:login'))
