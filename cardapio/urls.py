from django.urls import path
from . import views

urlpatterns = [
    # Rotas das Páginas Web
    path('', views.escolha_perfil, name='escolha_perfil'),
    path('usuario/', views.usuario_comum, name='usuario_comum'),
    path('login/', views.login_nutricionista, name='login_nutricionista'),
    path('dashboard/', views.dashboard_nutricionista, name='dashboard_nutricionista'),
    path('sair/', views.sair, name='sair'),
    
    # Rotas da API
    path('api/cardapios/', views.listar_cardapios, name='api_listar_cardapios'),
    path('api/cardapios/<int:pk>/', views.listar_cardapios, name='api_detalhar_cardapio'),
    
    path('api/dias/', views.dias_cardapio, name='api_listar_dias'),
    path('api/dias/<int:pk>/', views.dias_cardapio, name='api_detalhar_dia'),
    
    path('api/refeicoes/', views.refeicoes, name='api_listar_refeicoes'),
    path('api/refeicoes/<int:pk>/', views.refeicoes, name='api_detalhar_refeicao'),
    
    path('api/categorias/', views.categorias_item, name='api_listar_categorias'),
    path('api/categorias/<int:pk>/', views.categorias_item, name='api_detalhar_categoria'),
    
    path('api/itens/', views.itens_cardapio, name='api_listar_itens'),
    path('api/itens/<int:pk>/', views.itens_cardapio, name='api_detalhar_item'),
]