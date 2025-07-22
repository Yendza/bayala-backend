from rest_framework import serializers
from transaccoes.models import Transaccao

class TransaccaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccao
        fields = '__all__'  # Ou lista os campos que queres expor
