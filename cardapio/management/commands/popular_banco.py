import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from cardapio.models import DiaCardapio, Refeicao, CategoriaItem, ItemCardapio, Cardapio

class Command(BaseCommand):
    help = 'Popula o banco de dados com 2 semanas completas seguindo o padrão de categorias da UAN.'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Limpando dados antigos...")
        Cardapio.objects.all().delete()
        DiaCardapio.objects.all().delete()
        ItemCardapio.objects.all().delete()
        CategoriaItem.objects.all().delete()
        Refeicao.objects.all().delete()

        self.stdout.write("🍳 Criando Refeições...")
        cafe = Refeicao.objects.create(nome_refeicao="Café da Manhã")
        almoco = Refeicao.objects.create(nome_refeicao="Almoço")
        jantar = Refeicao.objects.create(nome_refeicao="Jantar")

        self.stdout.write("🏷️ Criando Categorias baseadas no padrão...")
        cat_bebida = CategoriaItem.objects.create(nome_categoria="Bebida")
        cat_alimento = CategoriaItem.objects.create(nome_categoria="Alimento")
        cat_entrada = CategoriaItem.objects.create(nome_categoria="Entrada")
        cat_prato_principal = CategoriaItem.objects.create(nome_categoria="Carne ou prep. com carne")
        cat_vegetariana = CategoriaItem.objects.create(nome_categoria="Opção Vegetariana")
        cat_guarnicao = CategoriaItem.objects.create(nome_categoria="Guarnição")
        cat_prato_base = CategoriaItem.objects.create(nome_categoria="Prato Base")
        cat_sobremesa = CategoriaItem.objects.create(nome_categoria="Sobremesa")

        self.stdout.write("🍎 Cadastrando itens do cardápio...")
        # Café
        i_cafe = ItemCardapio.objects.create(nome_item="Café; Iogurte", descricao="Café com leite e iogurte natural.")
        i_pao1 = ItemCardapio.objects.create(nome_item="Pão Doce; Pão de Mandioca", descricao="Pães frescos da padaria local.")
        i_pao2 = ItemCardapio.objects.create(nome_item="Pão Francês; Bolo de Aveia", descricao="Acompanha manteiga.")

        # Almoço
        i_entrada1 = ItemCardapio.objects.create(nome_item="Couve; Beterraba Cozida", descricao="Salada cozida e higienizada.")
        i_entrada2 = ItemCardapio.objects.create(nome_item="Alface; Cenoura Ralada", descricao="Salada fresca.")
        i_suino = ItemCardapio.objects.create(nome_item="Bife Suíno Grelhado", descricao="Temperado com ervas finas.")
        i_frango = ItemCardapio.objects.create(nome_item="Estrogonofe de Frango", descricao="Acompanha batata palha.")
        i_veg1 = ItemCardapio.objects.create(nome_item="Bife de Lentilha", descricao="Opção rica em ferro.")
        i_veg2 = ItemCardapio.objects.create(nome_item="Estrogonofe de Grão de Bico", descricao="Versão vegetariana.")
        i_guar1 = ItemCardapio.objects.create(nome_item="Virado de Abobrinha", descricao="Refogado tradicional.")
        i_guar2 = ItemCardapio.objects.create(nome_item="Inhame Chips", descricao="Assado e crocante.")
        i_arroz = ItemCardapio.objects.create(nome_item="Arroz Simples", descricao="Arroz branco cozido.")
        i_feijao = ItemCardapio.objects.create(nome_item="Feijão Simples", descricao="Feijão caldo grosso.")
        i_sobremesa1 = ItemCardapio.objects.create(nome_item="Mexerica Pokan", descricao="Fruta da estação.")
        i_sobremesa2 = ItemCardapio.objects.create(nome_item="Maçã", descricao="Fruta higienizada.")

        # Jantar
        i_j_entrada1 = ItemCardapio.objects.create(nome_item="Sopa de Ervilha", descricao="Sopa quente e nutritiva.")
        i_j_entrada2 = ItemCardapio.objects.create(nome_item="Salada de Tomate com Pepino", descricao="Salada leve e refrescante.")
        i_j_carne1 = ItemCardapio.objects.create(nome_item="Carne de Panela", descricao="Carne bovina cozida com legumes.")
        i_j_carne2 = ItemCardapio.objects.create(nome_item="Filé de Frango Grelhado", descricao="Filé temperado com limão.")
        i_j_veg1 = ItemCardapio.objects.create(nome_item="Torta de Legumes", descricao="Torta salgada sem carne.")
        i_j_veg2 = ItemCardapio.objects.create(nome_item="Omelete de Queijo", descricao="Omelete de forno.")
        i_j_guar1 = ItemCardapio.objects.create(nome_item="Purê de Batata", descricao="Purê cremoso feito com manteiga.")
        i_j_guar2 = ItemCardapio.objects.create(nome_item="Mandioca Cozida", descricao="Mandioca derretendo na manteiga.")

        self.stdout.write("📅 Gerando 14 dias (2 semanas completas)...")
        hoje = timezone.localtime(timezone.now()).date()
        dias_para_domingo = (hoje.weekday() + 1) % 7
        data_inicio = hoje - datetime.timedelta(days=dias_para_domingo)

        # Loop para criar 14 dias (de domingo da semana passada/atual até o sábado da próxima)
        for i in range(14):
            data_atual = data_inicio + datetime.timedelta(days=i)
            dia_obj = DiaCardapio.objects.create(data_dia=data_atual)

            # --- CAFÉ DA MANHÃ ---
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=cafe, id_categoria=cat_bebida, id_item=i_cafe)
            pao_do_dia = i_pao1 if i % 2 == 0 else i_pao2
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=cafe, id_categoria=cat_alimento, id_item=pao_do_dia)

            # --- ALMOÇO ---
            entrada_dia = i_entrada1 if i % 2 == 0 else i_entrada2
            carne_dia = i_suino if i % 2 == 0 else i_frango
            veg_dia = i_veg1 if i % 2 == 0 else i_veg2
            guar_dia = i_guar1 if i % 2 == 0 else i_guar2
            sob_dia = i_sobremesa1 if i % 2 == 0 else i_sobremesa2

            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_entrada, id_item=entrada_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_prato_principal, id_item=carne_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_vegetariana, id_item=veg_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_guarnicao, id_item=guar_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_prato_base, id_item=i_arroz)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_prato_base, id_item=i_feijao)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=almoco, id_categoria=cat_sobremesa, id_item=sob_dia)

            # --- JANTAR ---
            j_entrada_dia = i_j_entrada1 if i % 2 == 0 else i_j_entrada2
            j_carne_dia = i_j_carne1 if i % 2 == 0 else i_j_carne2
            j_veg_dia = i_j_veg1 if i % 2 == 0 else i_j_veg2
            j_guar_dia = i_j_guar1 if i % 2 == 0 else i_j_guar2

            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_entrada, id_item=j_entrada_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_prato_principal, id_item=j_carne_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_vegetariana, id_item=j_veg_dia)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_guarnicao, id_item=j_guar_dia)
            # Reaproveitando arroz, feijão e sobremesa do almoço para o jantar
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_prato_base, id_item=i_arroz)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_prato_base, id_item=i_feijao)
            Cardapio.objects.create(id_dia=dia_obj, id_refeicao=jantar, id_categoria=cat_sobremesa, id_item=sob_dia)

        data_fim = data_inicio + datetime.timedelta(days=13)
        self.stdout.write(self.style.SUCCESS(
            f'✅ Sucesso! 2 semanas geradas de {data_inicio.strftime("%d/%m/%Y")} até {data_fim.strftime("%d/%m/%Y")}.'
        ))