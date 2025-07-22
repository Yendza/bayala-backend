from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cotacao
from .serializers import CotacaoSerializer

class CotacaoViewSet(viewsets.ModelViewSet):
    queryset = Cotacao.objects.all().order_by('-data')
    serializer_class = CotacaoSerializer
    permission_classes = [IsAuthenticated]
