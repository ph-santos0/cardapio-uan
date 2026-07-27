from django.db import models
from django.core.exceptions import ValidationError

class Refeicao(models.Model):
    # unique=True impede que cadastrem duas refeições com o mesmo nome
    nome_refeicao = models.CharField(max_length=50, unique=True) 

    class Meta:
        db_table = 'refeicao'
        verbose_name = 'Refeição'
        verbose_name_plural = '2. Refeições'

    def __str__(self):
        return self.nome_refeicao

class CategoriaItem(models.Model):
    # unique=True impede duplicidade de categorias
    nome_categoria = models.CharField(max_length=50, unique=True) 

    class Meta:
        db_table = 'categoria_item'
        verbose_name = 'Categoria'
        verbose_name_plural = '3. Categorias'

    def __str__(self):
        return self.nome_categoria

class ItemCardapio(models.Model):
    # unique=True impede que cadastrem o mesmo alimento duas vezes
    nome_item = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'item_cardapio'
        verbose_name = 'Item do Cardápio'
        verbose_name_plural = '4. Itens do Cardápio'

    def __str__(self):
        return self.nome_item

class DiaCardapio(models.Model):
    # unique=True substitui a necessidade de validar conflitos de dias da antiga tabela de semanas
    data_dia = models.DateField(unique=True) 

    class Meta:
        db_table = 'dia_cardapio'
        ordering = ['-data_dia']
        verbose_name = 'Dia'
        verbose_name_plural = '1. Dias (Cardápio Diário)'

    def nome_dia(self):
        dias = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo']
        return dias[self.data_dia.weekday()]

    def __str__(self):
        return f"{self.nome_dia()} - {self.data_dia.strftime('%d/%m/%Y')}"

class Cardapio(models.Model):
    # O Dia continua CASCADE, pois se o dia for deletado, o cardápio dele deve sumir.
    id_dia = models.ForeignKey(DiaCardapio, on_delete=models.CASCADE)
    
    # PROTECT evita exclusão acidental de histórico!
    id_refeicao = models.ForeignKey(Refeicao, on_delete=models.PROTECT)
    id_categoria = models.ForeignKey(CategoriaItem, on_delete=models.PROTECT)
    id_item = models.ForeignKey(ItemCardapio, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cardapio'
        # Esta regra impede que a mesma comida seja lançada duas vezes na mesma categoria, refeição e dia!
        constraints = [
            models.UniqueConstraint(
                fields=['id_dia', 'id_refeicao', 'id_categoria', 'id_item'], 
                name='unique_cardapio_completo'
            )
        ]

    def __str__(self):
        return f"{self.id_dia} | {self.id_refeicao} | {self.id_categoria} | {self.id_item}"