from django.urls import path
from . import views


urlpatterns = [
    path('<int:chamado_id>/solucao/', views.registrar_solucao, name='registrar_solucao'),
    path('<int:chamado_id>/', views.detalhe_chamado, name='detalhe_chamado'),
    path('', views.listar_chamados, name='listar_chamados'),
    path('novo/', views.novo_chamado, name='novo_chamado'),
    path('<int:chamado_id>/status/', views.atualizar_status, name='atualizar_status'),
]