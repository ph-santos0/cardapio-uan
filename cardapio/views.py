from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from serializers import CardapioSerializer
from models import Cardapio
from rest_framework.response import Response

def escolha_perfil(request):
    return render(request, "cardapio/escolha_perfil.html")


def usuario_comum(request):
    return render(request, "cardapio/usuario_comum.html")


def login_nutricionista(request):
    erro = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect("dashboard_nutricionista")
        else:
            erro = "Usuário ou senha inválidos."

    return render(request, "cardapio/login_nutricionista.html", {"erro": erro})


@login_required
def dashboard_nutricionista(request):
    return render(request, "cardapio/dashboard_nutricionista.html")


def sair(request):
    logout(request)
    return redirect("escolha_perfil")


#crud
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def listar_cardapios(request):
    if request.method == 'GET':
        cardapios = Cardapio.objects.all()
        serializer = CardapioSerializer(cardapios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        novo_cardapio = CardapioSerializer(data=request.data)
        if novo_cardapio.isvalid():
            novo_cardapio.save()
            return Response(novo_cardapio.data, status=status.HTTP_201_CREATED)