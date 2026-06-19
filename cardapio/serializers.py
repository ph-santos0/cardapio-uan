from rest_framework import Serializers
from .models import Cardapio

class CardapioSerializer(Serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = '__all__'