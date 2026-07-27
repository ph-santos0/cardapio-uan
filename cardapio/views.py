import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Cardapio,
    CategoriaItem,
    DiaCardapio,
    ItemCardapio,
    Refeicao,
)

from .serializers import (
    CardapioSerializer,
    CategoriaItemSerializer,
    DiaCardapioSerializer,
    ItemCardapioSerializer,
    RefeicaoSerializer,
)


def escolha_perfil(request):
    return render(request, "cardapio/escolha_perfil.html")


def usuario_comum(request):
    # 1. Pega a data atual no fuso horário correto
    hoje = timezone.localtime(timezone.now()).date()

    # 2. Encontra as datas da semana atual (Domingo a Sábado)
    dias_para_domingo = (hoje.weekday() + 1) % 7
    data_inicio = hoje - datetime.timedelta(days=dias_para_domingo)
    data_fim = data_inicio + datetime.timedelta(days=6)

    # 3. Busca os cardápios vinculados aos dias dessa exata semana
    cardapios = (
        Cardapio.objects.select_related(
            "id_dia",
            "id_refeicao",
            "id_categoria",
            "id_item",
        )
        .filter(id_dia__data_dia__range=[data_inicio, data_fim])
        .order_by(
            "id_dia__data_dia",
            "id_refeicao__id_refeicao",
            "id_categoria__id_categoria",
            "id_item__nome_item",
        )
    )

    # O agrupamento agora é feito direto pelo HTML usando o {% regroup %}
    return render(
        request,
        "cardapio/usuario_comum.html",
        {
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "cardapios": cardapios,
        },
    )


def login_nutricionista(request):
    erro = None

    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard_nutricionista")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        usuario = authenticate(
            request,
            username=username,
            password=password,
        )

        if usuario is not None and usuario.is_staff:
            login(request, usuario)
            return redirect("dashboard_nutricionista")

        erro = "Usuário ou senha inválidos, ou usuário sem permissão de nutricionista."

    return render(
        request,
        "cardapio/login_nutricionista.html",
        {"erro": erro},
    )


@login_required(login_url="login_nutricionista")
def dashboard_nutricionista(request):
    if not request.user.is_staff:
        logout(request)
        return redirect("login_nutricionista")

    ultimos_cardapios = (
        Cardapio.objects.select_related(
            "id_dia",
            "id_refeicao",
            "id_categoria",
            "id_item",
        )
        .order_by("-id_cardapio")[:5]
    )

    return render(
        request,
        "cardapio/dashboard_nutricionista.html",
        {
            "total_dias": DiaCardapio.objects.count(),
            "total_refeicoes": Refeicao.objects.count(),
            "total_categorias": CategoriaItem.objects.count(),
            "total_itens": ItemCardapio.objects.count(),
            "total_cardapios": Cardapio.objects.count(),
            "ultimos_cardapios": ultimos_cardapios,
        },
    )


@require_POST
def sair(request):
    logout(request)
    return redirect("escolha_perfil")


def _crud_api(
    request,
    *,
    model,
    serializer_class,
    id_field,
    nome_entidade,
    pk=None,
    queryset=None,
):
    if request.method == "GET":
        if pk is not None:
            try:
                objeto = model.objects.get(**{id_field: pk})
            except model.DoesNotExist:
                return Response(
                    {"erro": f"{nome_entidade} não encontrado(a)."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                serializer_class(objeto).data,
                status=status.HTTP_200_OK,
            )

        objetos = queryset if queryset is not None else model.objects.all()
        return Response(
            serializer_class(objetos, many=True).data,
            status=status.HTTP_200_OK,
        )

    if request.method == "POST":
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    identificador = pk or request.data.get(id_field)

    if identificador is None:
        return Response(
            {"erro": f"Informe o campo {id_field} ou o ID na URL."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        objeto = model.objects.get(**{id_field: identificador})
    except model.DoesNotExist:
        return Response(
            {"erro": f"{nome_entidade} não encontrado(a)."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        serializer = serializer_class(objeto, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    objeto.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST", "PUT", "DELETE"])
def listar_cardapios(request, pk=None):
    queryset = Cardapio.objects.select_related(
        "id_dia",
        "id_refeicao",
        "id_categoria",
        "id_item",
    ).all()

    return _crud_api(
        request,
        model=Cardapio,
        serializer_class=CardapioSerializer,
        id_field="id_cardapio",
        nome_entidade="Cardápio",
        pk=pk,
        queryset=queryset,
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
def dias_cardapio(request, pk=None):
    return _crud_api(
        request,
        model=DiaCardapio,
        serializer_class=DiaCardapioSerializer,
        id_field="id_dia",
        nome_entidade="Dia do cardápio",
        pk=pk,
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
def refeicoes(request, pk=None):
    return _crud_api(
        request,
        model=Refeicao,
        serializer_class=RefeicaoSerializer,
        id_field="id_refeicao",
        nome_entidade="Refeição",
        pk=pk,
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
def categorias_item(request, pk=None):
    return _crud_api(
        request,
        model=CategoriaItem,
        serializer_class=CategoriaItemSerializer,
        id_field="id_categoria",
        nome_entidade="Categoria",
        pk=pk,
    )


@api_view(["GET", "POST", "PUT", "DELETE"])
def itens_cardapio(request, pk=None):
    return _crud_api(
        request,
        model=ItemCardapio,
        serializer_class=ItemCardapioSerializer,
        id_field="id_item",
        nome_entidade="Item do cardápio",
        pk=pk,
    )