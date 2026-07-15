from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CardapioSerializer, DiaCardapioSerializer, SemanaCardapioSerializer, RefeicaoSerializer, CategoriaItemSerializer, ItemCardapioSerializer
from .models import Cardapio, DiaCardapio, SemanaCardapio, Refeicao, CategoriaItem, ItemCardapio


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
        serializer = CardapioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dias_cardapio(request):
    if request.method == 'GET':
        dias_cardapio = DiaCardapio.objects.all()
        serializer = DiaCardapioSerializer(dias_cardapio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = DiaCardapioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id_dia = request.data.get('id_dia')
        try:
            dia_cardapio = DiaCardapio.objects.get(id_dia=id_dia)
        except DiaCardapio.DoesNotExist:
            return Response({'error': 'DiaCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiaCardapioSerializer(dia_cardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id_dia = request.data.get('id_dia')
        try:
            dia_cardapio = DiaCardapio.objects.get(id_dia=id_dia)
        except DiaCardapio.DoesNotExist:
            return Response({'error': 'DiaCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        dia_cardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def semanas_cardapio(request):
    if request.method == 'GET':
        semanas_cardapio = SemanaCardapio.objects.all()
        serializer = SemanaCardapioSerializer(semanas_cardapio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = SemanaCardapioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id_semana = request.data.get('id_semana')
        try:
            semana_cardapio = SemanaCardapio.objects.get(id_semana=id_semana)
        except SemanaCardapio.DoesNotExist:
            return Response({'error': 'SemanaCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SemanaCardapioSerializer(semana_cardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id_semana = request.data.get('id_semana')
        try:
            semana_cardapio = SemanaCardapio.objects.get(id_semana=id_semana)
        except SemanaCardapio.DoesNotExist:
            return Response({'error': 'SemanaCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        semana_cardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def refeicoes(request):
    if request.method == 'GET':
        refeicoes = Refeicao.objects.all()
        serializer = RefeicaoSerializer(refeicoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = RefeicaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id_refeicao = request.data.get('id_refeicao')
        try:
            refeicao = Refeicao.objects.get(id_refeicao=id_refeicao)
        except Refeicao.DoesNotExist:
            return Response({'error': 'Refeição não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RefeicaoSerializer(refeicao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id_refeicao = request.data.get('id_refeicao')
        try:
            refeicao = Refeicao.objects.get(id_refeicao=id_refeicao)
        except Refeicao.DoesNotExist:
            return Response({'error': 'Refeição não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        refeicao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def categorias_item(request):
    if request.method == 'GET':
        categorias_item = CategoriaItem.objects.all()
        serializer = CategoriaItemSerializer(categorias_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = CategoriaItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id_categoria = request.data.get('id_categoria')
        try:
            categoria_item = CategoriaItem.objects.get(id_categoria=id_categoria)
        except CategoriaItem.DoesNotExist:
            return Response({'error': 'CategoriaItem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaItemSerializer(categoria_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id_categoria = request.data.get('id_categoria')
        try:
            categoria_item = CategoriaItem.objects.get(id_categoria=id_categoria)
        except CategoriaItem.DoesNotExist:
            return Response({'error': 'CategoriaItem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        categoria_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def itens_cardapio(request):
    if request.method == 'GET':
        itens_cardapio = ItemCardapio.objects.all()
        serializer = ItemCardapioSerializer(itens_cardapio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = ItemCardapioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        id_item = request.data.get('id_item')
        try:
            item_cardapio = ItemCardapio.objects.get(id_item=id_item)
        except ItemCardapio.DoesNotExist:
            return Response({'error': 'ItemCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemCardapioSerializer(item_cardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        id_item = request.data.get('id_item')
        try:
            item_cardapio = ItemCardapio.objects.get(id_item=id_item)
        except ItemCardapio.DoesNotExist:
            return Response({'error': 'ItemCardapio não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item_cardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)