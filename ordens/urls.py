from django.urls import path
from .views import (
    PecasReadView,
    PecasCreateView,
    PecasUpdateView,
    PecasDeleteView,
    ServicosReadView,
    ServicosCreateView,
    ServicosUpdateView,
    ServicosDeleteView,
    VeiculosReadView,
    VeiculoCreateView,
    VeiculoUpdateView,
    VeiculoDeleteView,
    OrdemReadView,
    OrdemCreateView,
    OrdemUpdateView,
    OrdemDeleteView,
    OrdemPdfView
)

urlpatterns = [
    # Pecas
    path('pecas/', PecasReadView.as_view(), name='pecas_list'),
    path('pecas/criar/', PecasCreateView.as_view(), name='pecas_criar'),
    path('pecas/editar/<int:pk>/', PecasUpdateView.as_view(), name='pecas_atualizar'),
    path('pecas/excluir/<int:pk>/', PecasDeleteView.as_view(), name='pecas_excluir'),

    # Servicos
    path('servicos/', ServicosReadView.as_view(), name='servicos_list'),
    path('servicos/criar/', ServicosCreateView.as_view(), name='servicos_criar'),
    path('servicos/editar/<int:pk>/', ServicosUpdateView.as_view(), name='servicos_atualizar'),
    path('servicos/excluir/<int:pk>/', ServicosDeleteView.as_view(), name='servicos_excluir'),

    # Veiculos
    path('veiculos/', VeiculosReadView.as_view(), name='veiculos_list'),
    path('veiculos/cadastrar/', VeiculoCreateView.as_view(), name='cadastrar_veiculo'),
    path('veiculos/editar/<str:placa>/', VeiculoUpdateView.as_view(), name='veiculo_update'),
    path('veiculos/excluir/<str:placa>/', VeiculoDeleteView.as_view(), name='veiculo_delete'),

    # Ordens
    path("ordens/pdf/", OrdemPdfView.as_view(), name="ordem_pdf"),
    path('ordens/', OrdemReadView.as_view(), name='ordem_list'),
    path('ordens/criar/', OrdemCreateView.as_view(), name='ordem_criar'),
    path('ordens/editar/<int:pk>/', OrdemUpdateView.as_view(), name='ordem_atualizar'),
    path('ordens/excluir/<int:pk>/', OrdemDeleteView.as_view(), name='ordem_excluir'),
]
