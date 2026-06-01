from HttpResponse import Serializer
from .models import Cardapio

class CardapioSerializer(Serializer.CardapioSerializer):
    class Meta:
        model = Cardapio
        fields = '__all__'