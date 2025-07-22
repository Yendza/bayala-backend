from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_logado(request):
    usuario = request.user
    return Response({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
    })


class AlterarSenhaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        senha_actual = request.data.get('senha_actual')
        nova_senha = request.data.get('nova_senha')

        if not senha_actual or not nova_senha:
            return Response({'detail': 'Campos obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        utilizador = request.user

        if not utilizador.check_password(senha_actual):
            return Response({'detail': 'Senha atual incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

        utilizador.set_password(nova_senha)
        utilizador.save()

        # ✅ Blacklist todos os tokens existentes do utilizador
        tokens = OutstandingToken.objects.filter(user=utilizador)
        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except:
                pass

        return Response({'detail': 'Senha alterada com sucesso. Por favor, faça login novamente.'}, status=status.HTTP_200_OK)
