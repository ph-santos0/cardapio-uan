from datetime import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Cardapio,
    CategoriaItem,
    DiaCardapio,
    ItemCardapio,
    Refeicao,
    SemanaCardapio,
)


class UsuarioComumViewTests(TestCase):
    def criar_semana_com_item(self, inicio, fim, nome_item):
        semana = SemanaCardapio.objects.create(
            data_inicio=timezone.make_aware(datetime.combine(inicio, datetime.min.time())),
            data_fim=timezone.make_aware(datetime.combine(fim, datetime.max.time())),
        )
        dia = DiaCardapio.objects.create(
            id_semana=semana,
            data_dia=timezone.make_aware(datetime.combine(inicio, datetime.min.time())),
            nome_dia="Segunda-feira",
        )
        refeicao = Refeicao.objects.create(nome_refeicao=f"Almoço {nome_item}")
        categoria = CategoriaItem.objects.create(nome_categoria=f"Categoria {nome_item}")
        item = ItemCardapio.objects.create(nome_item=nome_item, descricao="Descrição")
        Cardapio.objects.create(
            id_dia=dia,
            id_refeicao=refeicao,
            id_categoria=categoria,
            id_item=item,
        )
        return semana

    @patch("cardapio.views.timezone.localdate")
    def test_exibe_semana_que_contem_a_data_local_atual(self, localdate_mock):
        localdate_mock.return_value = datetime(2026, 7, 23).date()
        semana_atual = self.criar_semana_com_item(
            datetime(2026, 7, 20).date(),
            datetime(2026, 7, 26).date(),
            "Arroz atual",
        )
        self.criar_semana_com_item(
            datetime(2026, 7, 27).date(),
            datetime(2026, 8, 2).date(),
            "Arroz futuro",
        )

        response = self.client.get(reverse("usuario_comum"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["semana"], semana_atual)
        self.assertContains(response, "Arroz atual")
        self.assertNotContains(response, "Arroz futuro")


class LogoutViewTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="nutricionista",
            password="senha-segura",
            is_staff=True,
        )
        self.client.login(username="nutricionista", password="senha-segura")

    def test_logout_nao_aceita_get(self):
        response = self.client.get(reverse("sair"))
        self.assertEqual(response.status_code, 405)

    def test_logout_aceita_post_e_encerra_sessao(self):
        response = self.client.post(reverse("sair"))
        self.assertRedirects(response, reverse("escolha_perfil"))
        self.assertNotIn("_auth_user_id", self.client.session)


class DashboardNutricionistaTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="nutricionista",
            password="senha-segura",
            is_staff=True,
        )
        self.client.login(username="nutricionista", password="senha-segura")

    def test_metricas_usam_rotulos_semanticos_corretos(self):
        response = self.client.get(reverse("dashboard_nutricionista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cardápios Semanais")
        self.assertContains(response, "Composições do Cardápio")
        self.assertNotContains(response, "Cardápios cadastrados")
