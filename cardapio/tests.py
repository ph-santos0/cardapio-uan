from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from datetime import date
from rest_framework import status
from rest_framework.test import APIClient

from .models import DiaCardapio, Refeicao, CategoriaItem, ItemCardapio, Cardapio

class SistemaCardapioTests(TestCase):
    def setUp(self):
        # Clientes para simular o navegador e requisições à API
        self.client = Client()
        self.api_client = APIClient()

        # Criar usuário autorizado
        self.nutri = User.objects.create_user(username='nutricionista', password='123', is_staff=True)

        # -----------------------------------------------------------
        # TESTE: Cadastrar dia, refeição, categoria e item
        # Resultado esperado: Registros salvos sem erros no banco
        # -----------------------------------------------------------
        self.dia = DiaCardapio.objects.create(data_dia=date.today())
        self.refeicao = Refeicao.objects.create(nome_refeicao="Almoço Teste")
        self.categoria = CategoriaItem.objects.create(nome_categoria="Prato Principal Teste")
        self.item = ItemCardapio.objects.create(nome_item="Frango Teste", descricao="Teste")

        # -----------------------------------------------------------
        # TESTE: Montar cardápio
        # Resultado esperado: Registro salvo no banco com sucesso
        # -----------------------------------------------------------
        self.cardapio = Cardapio.objects.create(
            id_dia=self.dia,
            id_refeicao=self.refeicao,
            id_categoria=self.categoria,
            id_item=self.item
        )

    def test_acesso_pagina_publica_sem_login(self):
        """ TESTE: Acessar página pública sem login | Resultado: Acesso permitido (HTTP 200) """
        response = self.client.get(reverse('usuario_comum'))
        self.assertEqual(response.status_code, 200)

    def test_acesso_dashboard_sem_login(self):
        """ TESTE: Acessar dashboard sem login | Resultado: Redirecionamento para login (HTTP 302) """
        response = self.client.get(reverse('dashboard_nutricionista'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login_nutricionista')))

    def test_entrar_com_nutricionista_autorizado(self):
        """ TESTE: Entrar com nutricionista autorizado | Resultado: Painel carregado (HTTP 200) """
        self.client.login(username='nutricionista', password='123')
        response = self.client.get(reverse('dashboard_nutricionista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Área administrativa")

    def test_impedir_cardapio_duplicado(self):
        """ TESTE: Repetir a mesma combinação | Resultado: Duplicidade recusada (IntegrityError) """
        with self.assertRaises(IntegrityError):
            Cardapio.objects.create(
                id_dia=self.dia,
                id_refeicao=self.refeicao,
                id_categoria=self.categoria,
                id_item=self.item
            )

    def test_exclusao_controlada(self):
        """ TESTE: Excluir registro histórico | Resultado: Exclusão recusada (ProtectedError) """
        # Tentar apagar um item que já está em uso em um cardápio montado
        with self.assertRaises(ProtectedError):
            self.item.delete()

    def test_editar_cardapio(self):
        """ TESTE: Editar cardápio | Resultado: Alteração salva e exibida """
        novo_item = ItemCardapio.objects.create(nome_item="Bife Teste")
        self.cardapio.id_item = novo_item
        self.cardapio.save()
        self.assertEqual(self.cardapio.id_item.nome_item, "Bife Teste")

    def test_api_post_anonimo_bloqueado(self):
        """ TESTE: Enviar POST anônimo à API | Resultado: Acesso bloqueado (HTTP 403 Forbidden) """
        response = self.api_client.post(reverse('api_listar_cardapios'), {}) # URL corrigida aqui
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_anonimo_bloqueado(self):
        """ TESTE: Enviar DELETE anônimo à API | Resultado: Acesso bloqueado (HTTP 403 Forbidden) """
        response = self.api_client.delete(reverse('api_listar_cardapios')) # URL corrigida aqui
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_nova_arquitetura_impede_erros_de_data(self):
        """
        Substitui os testes 'Semana com data invertida' e 'Dia fora da semana'.
        A nova arquitetura remove a tabela 'Semana', mas impede dias duplicados.
        """
        with self.assertRaises(IntegrityError):
            DiaCardapio.objects.create(data_dia=date.today()) # Tentar criar a mesma data de novo