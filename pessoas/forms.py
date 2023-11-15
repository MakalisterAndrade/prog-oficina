from django import forms
from .models import Endereco, Cliente, Equipe, Mecanico


class ClienteForm(forms.Form):

    nome = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=15)
    cep = forms.IntegerField()
    rua = forms.CharField(max_length=255)
    bairro = forms.CharField(max_length=255)
    numero = forms.IntegerField()
    complemento = forms.CharField(max_length=255, required=False)
    cidade = forms.CharField(max_length=255)
    estado = forms.ChoiceField(choices=Endereco.estados, widget=forms.Select(attrs={'class': 'form-control'}))


class MecanicoForm(forms.Form):

    nome = forms.CharField(max_length=255)
    especialidade = forms.CharField(max_length=255)

    cep = forms.IntegerField()
    rua = forms.CharField(max_length=255)
    bairro = forms.CharField(max_length=255)
    numero = forms.IntegerField()
    complemento = forms.CharField(max_length=255, required=False)
    cidade = forms.CharField(max_length=255)
    estado = forms.ChoiceField(choices=Endereco.estados, widget=forms.Select(attrs={'class': 'form-control'}))


class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['descricao', 'mecanicos']
        labels = {'mecanicos': 'Mecânicos', 'descricao': 'Descrição'}
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control mb-4'}),
            'mecanicos': forms.SelectMultiple(attrs={'class': 'form-select mb-4'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mecanicos'].queryset = Mecanico.objects.all()
