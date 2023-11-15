from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    MecanicoListView, MecanicoCreateView, MecanicoUpdateView, MecanicoDeleteView,
    EquipeListView, EquipeCreateView, EquipeUpdateView, EquipeDeleteView,
)

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='clientes_list'),
    path('clientes/criar/', ClienteCreateView.as_view(), name='clientes_criar'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='clientes_atualizar'),
    path('clientes/excluir/<int:pk>/', ClienteDeleteView.as_view(), name='clientes_excluir'),

    path('mecanicos/', MecanicoListView.as_view(), name='mecanicos_list'),
    path('mecanicos/criar/', MecanicoCreateView.as_view(), name='mecanicos_criar'),
    path('mecanicos/editar/<int:pk>/', MecanicoUpdateView.as_view(), name='mecanicos_atualizar'),
    path('mecanicos/excluir/<int:pk>/', MecanicoDeleteView.as_view(), name='mecanicos_excluir'),

    path('equipes/', EquipeListView.as_view(), name='equipes_list'),
    path('equipes/criar/', EquipeCreateView.as_view(), name='equipes_criar'),
    path('equipes/editar/<int:pk>/', EquipeUpdateView.as_view(), name='equipes_atualizar'),
    path('equipes/excluir/<int:pk>/', EquipeDeleteView.as_view(), name='equipes_excluir'),
]
