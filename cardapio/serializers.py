from rest_framework import serializers
from .models import Cardapio, DiaCardapio, SemanaCardapio, Refeicao, CategoriaItem, ItemCardapio

class CardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = '__all__'

class DiaCardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaCardapio
        fields = '__all__'

class SemanaCardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemanaCardapio
        fields = '__all__' 

class RefeicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refeicao
        fields = '__all__'

class CategoriaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaItem
        fields = '__all__'

class ItemCardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCardapio
        fields = '__all__'