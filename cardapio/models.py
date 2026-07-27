from django.db import models

class DiaCardapio(models.Model):
    id_dia = models.AutoField(primary_key=True)
    data_dia = models.DateField(unique=True, verbose_name="Data do Dia")

    class Meta:
            db_table = 'dia_cardapio'
            ordering = ['-data_dia']
            verbose_name = 'Dia'
            verbose_name_plural = '1. Cardápio Diário'

    def nome_dia(self):
        # Calcula o nome do dia dinamicamente com base na data
        nomes = {
            0: 'Segunda-Feira', 1: 'Terça-Feira', 2: 'Quarta-Feira',
            3: 'Quinta-Feira', 4: 'Sexta-Feira', 5: 'Sábado', 6: 'Domingo'
        }
        return nomes[self.data_dia.weekday()]

    def __str__(self):
        return f"{self.nome_dia()} ({self.data_dia.strftime('%d/%m/%Y')})"

class Refeicao(models.Model):
    id_refeicao = models.AutoField(primary_key=True)
    nome_refeicao = models.CharField(max_length=50)

    class Meta:
            db_table = 'refeicao'
            verbose_name = 'Refeição'
            verbose_name_plural = '2. Refeições'

    def __str__(self):
        return self.nome_refeicao

class CategoriaItem(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=50)

    class Meta:
            db_table = 'categoria_item'
            verbose_name = 'Categoria'
            verbose_name_plural = '3. Categorias'

    def __str__(self):
        return self.nome_categoria

class ItemCardapio(models.Model):
    id_item = models.AutoField(primary_key=True)
    nome_item = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
            db_table = 'item_cardapio'
            verbose_name = 'Item do Cardápio'
            verbose_name_plural = '4. Itens do Cardápio'

    def __str__(self):
        return self.nome_item

class Cardapio(models.Model):
    id_cardapio = models.AutoField(primary_key=True)
    id_dia = models.ForeignKey(DiaCardapio, on_delete=models.CASCADE, db_column='id_dia', related_name='cardapios')
    id_refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE, db_column='id_refeicao')
    id_categoria = models.ForeignKey(CategoriaItem, on_delete=models.CASCADE, db_column='id_categoria')
    id_item = models.ForeignKey(ItemCardapio, on_delete=models.CASCADE, db_column='id_item')

    class Meta:
        db_table = 'cardapio'
        
    def __str__(self):
        return f"Cardápio - {self.id_dia} - {self.id_refeicao}"