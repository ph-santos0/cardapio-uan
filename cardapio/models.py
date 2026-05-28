from django.db import models


class SemanaCardapio(models.Model):
    id_semana = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    class Meta:
        db_table = 'semana_cardapio'

    def __str__(self):
        return f"{self.data_inicio} até {self.data_fim}"


class DiaCardapio(models.Model):
    id_dia = models.AutoField(primary_key=True)

    id_semana = models.ForeignKey(
        SemanaCardapio,
        on_delete=models.CASCADE,
        db_column='id_semana',
        related_name='dias'
    )

    data_dia = models.DateTimeField()

    nome_dia = models.CharField(
        max_length=20
    )

    class Meta:
        db_table = 'dia_cardapio'

    def __str__(self):
        return self.nome_dia


class Refeicao(models.Model):
    id_refeicao = models.AutoField(primary_key=True)

    nome_refeicao = models.CharField(
        max_length=50
    )

    class Meta:
        db_table = 'refeicao'

    def __str__(self):
        return self.nome_refeicao


class CategoriaItem(models.Model):
    id_categoria = models.AutoField(primary_key=True)

    nome_categoria = models.CharField(
        max_length=50
    )

    class Meta:
        db_table = 'categoria_item'

    def __str__(self):
        return self.nome_categoria


class ItemCardapio(models.Model):
    id_item = models.AutoField(primary_key=True)

    nome_item = models.CharField(
        max_length=50
    )

    descricao = models.CharField(
        max_length=255
    )

    class Meta:
        db_table = 'item_cardapio'

    def __str__(self):
        return self.nome_item


class Cardapio(models.Model):
    id_cardapio = models.AutoField(primary_key=True)

    id_dia = models.ForeignKey(
        DiaCardapio,
        on_delete=models.CASCADE,
        db_column='id_dia'
    )

    id_refeicao = models.ForeignKey(
        Refeicao,
        on_delete=models.CASCADE,
        db_column='id_refeicao'
    )

    id_categoria = models.ForeignKey(
        CategoriaItem,
        on_delete=models.CASCADE,
        db_column='id_categoria'
    )

    id_item = models.ForeignKey(
        ItemCardapio,
        on_delete=models.CASCADE,
        db_column='id_item'
    )

    class Meta:
        db_table = 'cardapio'

    def __str__(self):
        return f"{self.id_dia} - {self.id_refeicao}"