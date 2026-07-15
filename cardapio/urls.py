from django.contrib import admin
from django.urls import include, path
from .views import dias_cardapio, listar_cardapios, itens_cardapio, refeicoes, categorias_item, itens_cardapio, semanas_cardapio

urlpatterns = [
    path("cardapios/", listar_cardapios, name="listar_cardapios"),
    path("dia_cardapio/", dias_cardapio, name="dias_cardapio"),
    path('dia_cardapio/<int:pk>/', dias_cardapio, name='dias_cardapio'),
    path("semanas_cardapio/", semanas_cardapio, name="semanas_cardapio"),
    path('semanas_cardapio/<int:pk>/', semanas_cardapio, name='semanas_cardapio'),
    path("refeicoes/", refeicoes, name="refeicoes"),
    path('refeicoes/<int:pk>/', refeicoes, name='refeicoes'),
    path("categorias_item/", categorias_item, name="categorias_item"),
    path('categorias_item/<int:pk>/', categorias_item, name='categorias_item'),
    path("itens_cardapio/", itens_cardapio, name="listar_itens_cardapio"),
    path('itens_cardapio/<int:pk>/', itens_cardapio, name='itens_cardapio'),
]   