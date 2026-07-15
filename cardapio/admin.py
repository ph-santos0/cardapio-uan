from django.contrib import admin

from .models import (
    SemanaCardapio,
    DiaCardapio,
    Refeicao,
    CategoriaItem,
    ItemCardapio,
    Cardapio,
)


@admin.register(SemanaCardapio)
class SemanaCardapioAdmin(admin.ModelAdmin):
    list_display = ("id_semana", "data_inicio", "data_fim")
    ordering = ("-data_inicio",)


@admin.register(DiaCardapio)
class DiaCardapioAdmin(admin.ModelAdmin):
    list_display = ("id_dia", "nome_dia", "data_dia", "id_semana")
    list_filter = ("id_semana",)
    search_fields = ("nome_dia",)


@admin.register(Refeicao)
class RefeicaoAdmin(admin.ModelAdmin):
    list_display = ("id_refeicao", "nome_refeicao")
    search_fields = ("nome_refeicao",)


@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ("id_categoria", "nome_categoria")
    search_fields = ("nome_categoria",)


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ("id_item", "nome_item", "descricao")
    search_fields = ("nome_item", "descricao")


@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = (
        "id_cardapio",
        "id_dia",
        "id_refeicao",
        "id_categoria",
        "id_item",
    )

    list_filter = (
        "id_dia",
        "id_refeicao",
        "id_categoria",
    )

    search_fields = (
        "id_item__nome_item",
        "id_dia__nome_dia",
        "id_refeicao__nome_refeicao",
    )