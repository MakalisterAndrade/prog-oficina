from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from pessoas.forms import ClienteForm, MecanicoForm, EquipeForm
from pessoas.models import Cliente, Mecanico, Equipe, Pessoa, Endereco
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreateViewBase(LoginRequiredMixin, FormView):
    template_name = None
    form_class = None
    success_url = None
    model = None
    success_message = None

    def form_valid(self, form):
        endereco = Endereco.objects.create(
            cep=form.cleaned_data['cep'],
            rua=form.cleaned_data['rua'],
            bairro=form.cleaned_data['bairro'],
            numero=form.cleaned_data['numero'],
            complemento=form.cleaned_data['complemento'],
            cidade=form.cleaned_data['cidade'],
            estado=form.cleaned_data['estado']
        )

        pessoa = Pessoa.objects.create(
            nome=form.cleaned_data['nome'],
            endereco=endereco
        )

        self.model.objects.create(
            pessoa=pessoa,
            **self.get_model_specific_fields(form.cleaned_data)
        )

        messages.success(self.request, self.success_message)
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, f'Erro ao cadastrar o(a) {self.model._meta.verbose_name}.')
        return super().form_invalid(form)

    def get_model_specific_fields(self, cleaned_data):
        raise NotImplementedError("Método get_model_specific_fields deve ser implementado nas subclasses.")


class ClienteCreateView(CreateViewBase):
    template_name = 'cliente/create.html'
    form_class = ClienteForm
    success_url = reverse_lazy('clientes_list')
    model = Cliente
    success_message = 'Cliente adicionado.'

    def get_model_specific_fields(self, cleaned_data):
        return {'telefone': cleaned_data['telefone']}


class MecanicoCreateView(CreateViewBase):
    template_name = 'mecanico/create.html'
    form_class = MecanicoForm
    success_url = reverse_lazy('mecanicos_list')
    model = Mecanico
    success_message = 'Mecânico adicionado.'

    def get_model_specific_fields(self, cleaned_data):
        return {'especialidade': cleaned_data['especialidade']}


class UpdateViewBase(LoginRequiredMixin, FormView):
    template_name = None
    form_class = None
    success_url = None
    model = None
    specific_model_fields = None
    success_message = None

    def get_object(self):
        try:
            return self.model.objects.get(pk=self.kwargs['pk'])
        except self.model.DoesNotExist:
            messages.error(self.request, f'O {self.model._meta.verbose_name} não existe!')
            return reverse('clientes_list')  # Redirecione para a lista se o objeto não existir

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.model._meta.verbose_name] = self.get_object()
        context['estado'] = context[self.model._meta.verbose_name].pessoa.endereco.estado  # BUG
        return context

    def form_valid(self, form):
        obj = self.get_object()
        pessoa = obj.pessoa
        endereco = pessoa.endereco

        for field in self.specific_model_fields:
            setattr(endereco, field, form.cleaned_data[field])

        pessoa.nome = form.cleaned_data['nome']
        pessoa.save()

        self.update_model_specific_fields(obj, form.cleaned_data)

        messages.success(self.request, f'{self.model._meta.verbose_name.capitalize()} atualizado(a).')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'Erro ao atualizar o(a) {self.model._meta.verbose_name}.')
        return super().form_invalid(form)

    def update_model_specific_fields(self, obj, cleaned_data):
        raise NotImplementedError("Método update_model_specific_fields deve ser implementado nas subclasses.")


class ClienteUpdateView(UpdateViewBase):
    template_name = 'cliente/edit.html'
    form_class = ClienteForm
    success_url = reverse_lazy('clientes_list')
    model = Cliente
    specific_model_fields = ['cep', 'rua', 'bairro', 'numero', 'complemento', 'cidade', 'estado', 'telefone']
    success_message = 'Cliente atualizado.'

    def update_model_specific_fields(self, obj, cleaned_data):
        obj.telefone = cleaned_data['telefone']
        obj.save()


class MecanicoUpdateView(UpdateViewBase):
    template_name = 'mecanico/edit.html'
    form_class = MecanicoForm
    success_url = reverse_lazy('mecanicos_list')
    model = Mecanico
    specific_model_fields = ['cep', 'rua', 'bairro', 'numero', 'complemento', 'cidade', 'estado', 'especialidade']
    success_message = 'Mecânico atualizado.'

    def update_model_specific_fields(self, obj, cleaned_data):
        obj.especialidade = cleaned_data['especialidade']
        obj.save()


class DeleteViewBase(LoginRequiredMixin, DeleteView):
    model = None
    template_name = None
    success_url = None
    success_message = None

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ClienteDeleteView(DeleteViewBase):
    model = Cliente
    template_name = 'cliente/delete.html'
    success_url = reverse_lazy('clientes_list')
    success_message = 'Cliente excluído.'


class MecanicoDeleteView(DeleteViewBase):
    model = Mecanico
    template_name = 'mecanico/delete.html'
    success_url = reverse_lazy('mecanicos_list')
    success_message = 'Mecânico excluído.'

class ClienteListView(LoginRequiredMixin,ListView):
    model = Cliente
    ordering = ['-pessoa_id']
    context_object_name = 'clientes'
    template_name = 'cliente/list.html'
    paginate_by = 10

class MecanicoListView(LoginRequiredMixin, ListView):
    model = Mecanico
    ordering = ['-pessoa_id']
    context_object_name = 'mecanicos'
    template_name = 'mecanico/list.html'
    paginate_by = 20

class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    context_object_name = 'equipes'
    ordering = ['-id']
    template_name = 'equipes/list.html'
    paginate_by = 10


class EquipeCreateView(LoginRequiredMixin, FormView):
    form_class = EquipeForm
    template_name = 'equipes/create.html'
    success_url = reverse_lazy('equipes_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Equipe adicionada.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar a equipe.')
        return super().form_invalid(form)


class EquipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipe
    form_class = EquipeForm
    template_name = 'equipes/edit.html'
    success_url = reverse_lazy('equipes_list')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'


class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    template_name = 'equipes/delete.html'
    success_url = reverse_lazy('equipes_list')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
