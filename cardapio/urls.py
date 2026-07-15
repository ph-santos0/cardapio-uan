from django.urls import path

from .views import (
    categorias_item,
    dashboard_nutricionista,
    dias_cardapio,
    escolha_perfil,
    itens_cardapio,
    listar_cardapios,
    login_nutricionista,
    refeicoes,
    sair,
    semanas_cardapio,
    usuario_comum,
)

urlpatterns = [
    path("", escolha_perfil, name="escolha_perfil"),
    path("usuario/", usuario_comum, name="usuario_comum"),
    path("login/", login_nutricionista, name="login_nutricionista"),
    path("dashboard/", dashboard_nutricionista, name="dashboard_nutricionista"),
    path("sair/", sair, name="sair"),

    path("cardapios/", listar_cardapios, name="listar_cardapios"),
    path("cardapios/<int:pk>/", listar_cardapios, name="detalhar_cardapio"),

    path("dia_cardapio/", dias_cardapio, name="dias_cardapio"),
    path("dia_cardapio/<int:pk>/", dias_cardapio, name="detalhar_dia_cardapio"),

    path("semanas_cardapio/", semanas_cardapio, name="semanas_cardapio"),
    path(
        "semanas_cardapio/<int:pk>/",
        semanas_cardapio,
        name="detalhar_semana_cardapio",
    ),

    path("refeicoes/", refeicoes, name="refeicoes"),
    path("refeicoes/<int:pk>/", refeicoes, name="detalhar_refeicao"),

    path("categorias_item/", categorias_item, name="categorias_item"),
    path(
        "categorias_item/<int:pk>/",
        categorias_item,
        name="detalhar_categoria_item",
    ),

    path("itens_cardapio/", itens_cardapio, name="listar_itens_cardapio"),
    path(
        "itens_cardapio/<int:pk>/",
        itens_cardapio,
        name="detalhar_item_cardapio",
    ),
]
