from django.contrib import admin

# Register your models here.
import cardapio.models as models

admin.site.register(models.SemanaCardapio)
admin.site.register(models.DiaCardapio)
admin.site.register(models.Refeicao)
admin.site.register(models.CategoriaItem)
admin.site.register(models.ItemCardapio)