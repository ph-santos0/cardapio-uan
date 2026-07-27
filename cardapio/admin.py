from django.contrib import admin
from .models import (
    DiaCardapio,
    Refeicao,
    CategoriaItem,
    ItemCardapio,
    Cardapio,
)

class CardapioInline(admin.TabularInline):
    model = Cardapio
    extra = 5  
@admin.register(DiaCardapio)
class DiaCardapioAdmin(admin.ModelAdmin):
    list_display = ("id_dia", "data_dia", "nome_dia_dinamico")
    ordering = ("-data_dia",)
    date_hierarchy = "data_dia"
    
    inlines = [CardapioInline] 

    def nome_dia_dinamico(self, obj):
        return obj.nome_dia()
    nome_dia_dinamico.short_description = "Dia da Semana"


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
        "id_refeicao__nome_refeicao",
    )
    
    def has_module_permission(self, request):
        return False