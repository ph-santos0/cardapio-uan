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
    list_display = ("id", "data_dia", "nome_dia_dinamico") # Corrigido id_dia para id
    ordering = ("-data_dia",)
    date_hierarchy = "data_dia"
    
    inlines = [CardapioInline] 

    def nome_dia_dinamico(self, obj):
        return obj.nome_dia()
    nome_dia_dinamico.short_description = "Dia da Semana"


@admin.register(Refeicao)
class RefeicaoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_refeicao") # Corrigido id_refeicao para id
    search_fields = ("nome_refeicao",)


@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_categoria") # Corrigido id_categoria para id
    search_fields = ("nome_categoria",)


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_item", "descricao") # Corrigido id_item para id
    search_fields = ("nome_item", "descricao")


@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = (
        "id", # Corrigido id_cardapio para id
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