from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_chamados, name='listar_chamados'),
    path('novo/', views.novo_chamado, name='novo_chamado'),
    path('<int:chamado_id>/status/', views.atualizar_status,name='atualizar_status'),
]