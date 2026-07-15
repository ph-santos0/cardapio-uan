from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Cardapio,
    CategoriaItem,
    DiaCardapio,
    ItemCardapio,
    Refeicao,
    SemanaCardapio,
)
from .serializers import CardapioSerializer


def escolha_perfil(request):
    return render(
        request,
        "cardapio/escolha_perfil.html",
    )


def usuario_comum(request):
    registros = Cardapio.objects.select_related(
        "id_dia",
        "id_dia__id_semana",
        "id_refeicao",
        "id_categoria",
        "id_item",
    ).order_by(
        "id_dia__data_dia",
        "id_refeicao__id_refeicao",
        "id_categoria__id_categoria",
        "id_item__nome_item",
    )

    dias_organizados = OrderedDict()

    for registro in registros:
        dia = registro.id_dia
        refeicao = registro.id_refeicao

        if dia.id_dia not in dias_organizados:
            dias_organizados[dia.id_dia] = {
                "nome": dia.nome_dia,
                "data": dia.data_dia,
                "semana": dia.id_semana,
                "refeicoes": OrderedDict(),
            }

        refeicoes_do_dia = dias_organizados[dia.id_dia]["refeicoes"]

        if refeicao.id_refeicao not in refeicoes_do_dia:
            refeicoes_do_dia[refeicao.id_refeicao] = {
                "nome": refeicao.nome_refeicao,
                "itens": [],
            }

        refeicoes_do_dia[refeicao.id_refeicao]["itens"].append(
            {
                "nome": registro.id_item.nome_item,
                "descricao": registro.id_item.descricao,
                "categoria": registro.id_categoria.nome_categoria,
            }
        )

    dias = []

    for dia in dias_organizados.values():
        dia["refeicoes"] = list(dia["refeicoes"].values())
        dias.append(dia)

    semana = None

    if dias:
        semana = dias[0]["semana"]

    contexto = {
        "dias": dias,
        "semana": semana,
    }

    return render(
        request,
        "cardapio/usuario_comum.html",
        contexto,
    )


def login_nutricionista(request):
    erro = None

    if request.user.is_authenticated:
        return redirect("dashboard_nutricionista")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        usuario = authenticate(
            request,
            username=username,
            password=password,
        )

        if usuario is not None:
            login(request, usuario)
            return redirect("dashboard_nutricionista")

        erro = "Usuário ou senha inválidos."

    return render(
        request,
        "cardapio/login_nutricionista.html",
        {
            "erro": erro,
        },
    )


@login_required(login_url="login_nutricionista")
def dashboard_nutricionista(request):
    ultimos_cardapios = Cardapio.objects.select_related(
        "id_dia",
        "id_refeicao",
        "id_categoria",
        "id_item",
    ).order_by("-id_cardapio")[:5]

    contexto = {
        "total_semanas": SemanaCardapio.objects.count(),
        "total_dias": DiaCardapio.objects.count(),
        "total_refeicoes": Refeicao.objects.count(),
        "total_categorias": CategoriaItem.objects.count(),
        "total_itens": ItemCardapio.objects.count(),
        "total_cardapios": Cardapio.objects.count(),
        "ultimos_cardapios": ultimos_cardapios,
    }

    return render(
        request,
        "cardapio/dashboard_nutricionista.html",
        contexto,
    )


def sair(request):
    logout(request)
    return redirect("escolha_perfil")


@api_view(["GET"])
def listar_cardapios(request):
    cardapios = Cardapio.objects.select_related(
        "id_dia",
        "id_refeicao",
        "id_categoria",
        "id_item",
    ).all()

    serializer = CardapioSerializer(
        cardapios,
        many=True,
    )

    return Response(serializer.data)