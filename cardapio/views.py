from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status
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
from .serializers import (
    CardapioSerializer,
    CategoriaItemSerializer,
    DiaCardapioSerializer,
    ItemCardapioSerializer,
    RefeicaoSerializer,
    SemanaCardapioSerializer,
)


def escolha_perfil(request):
    return render(request, "cardapio/escolha_perfil.html")


def usuario_comum(request):
    ultimo_registro = (
        Cardapio.objects.select_related("id_dia__id_semana")
        .order_by("-id_dia__data_dia", "-id_cardapio")
        .first()
    )

    semana = ultimo_registro.id_dia.id_semana if ultimo_registro else None

    if semana is None:
        registros = Cardapio.objects.none()
    else:
        registros = (
            Cardapio.objects.select_related(
                "id_dia",
                "id_dia__id_semana",
                "id_refeicao",
                "id_categoria",
                "id_item",
            )
            .filter(id_dia__id_semana=semana)
            .order_by(
                "id_dia__data_dia",
                "id_refeicao__id_refeicao",
                "id_categoria__id_categoria",
                "id_item__nome_item",
            )
        )

    dias_organizados = OrderedDict()

    for registro in registros:
        dia = registro.id_dia
        refeicao = registro.id_refeicao

        if dia.id_dia not in dias_organizados:
            dias_organizados[dia.id_dia] = {
                "nome": dia.nome_dia,
                "data": dia.data_dia,
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

    return render(
        request,
        "cardapio/usuario_comum.html",
        {
            "dias": dias,
            "semana": semana,
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
            "total_semanas": SemanaCardapio.objects.count(),
            "total_dias": DiaCardapio.objects.count(),
            "total_refeicoes": Refeicao.objects.count(),
            "total_categorias": CategoriaItem.objects.count(),
            "total_itens": ItemCardapio.objects.count(),
            "total_cardapios": Cardapio.objects.count(),
            "ultimos_cardapios": ultimos_cardapios,
        },
    )


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
def semanas_cardapio(request, pk=None):
    return _crud_api(
        request,
        model=SemanaCardapio,
        serializer_class=SemanaCardapioSerializer,
        id_field="id_semana",
        nome_entidade="Semana do cardápio",
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
