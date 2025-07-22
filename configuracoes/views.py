from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import JSONParser

class GerirUtilizadoresView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        data = []
        for u in users:
            data.append({
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'is_staff': u.is_staff,
                'is_superuser': u.is_superuser,
                'last_login': u.last_login,
                'date_joined': u.date_joined,
                'groups': [g.name for g in u.groups.all()],
                'user_permissions': [p.codename for p in u.user_permissions.all()]
            })
        return Response(data)

    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Username já existe'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=data.get('username'),
            email=data.get('email', ''),
            is_staff=data.get('is_staff', False),
            is_superuser=data.get('is_superuser', False),
            password=make_password(data.get('password')),
        )
        # Associar grupos e permissões se passados
        groups = data.get('groups', [])
        for group_name in groups:
            group = Group.objects.filter(name=group_name).first()
            if group:
                user.groups.add(group)

        permissions = data.get('user_permissions', [])
        for perm_codename in permissions:
            perm = Permission.objects.filter(codename=perm_codename).first()
            if perm:
                user.user_permissions.add(perm)

        user.save()
        return Response({'msg': 'Utilizador criado com sucesso'}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilizador não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.is_staff = data.get('is_staff', user.is_staff)
        user.is_superuser = data.get('is_superuser', user.is_superuser)

        password = data.get('password', None)
        if password:
            user.password = make_password(password)

        user.groups.clear()
        groups = data.get('groups', [])
        for group_name in groups:
            group = Group.objects.filter(name=group_name).first()
            if group:
                user.groups.add(group)

        user.user_permissions.clear()
        permissions = data.get('user_permissions', [])
        for perm_codename in permissions:
            perm = Permission.objects.filter(codename=perm_codename).first()
            if perm:
                user.user_permissions.add(perm)

        user.save()
        return Response({'msg': 'Utilizador atualizado com sucesso'})

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'msg': 'Utilizador apagado com sucesso'})
        except User.DoesNotExist:
            return Response({'error': 'Utilizador não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class GerirPermissoesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        permissions = Permission.objects.all()
        data = [{'id': p.id, 'name': p.name, 'codename': p.codename, 'content_type': str(p.content_type)} for p in permissions]
        return Response(data)

    def post(self, request):
        return Response({'error': 'Criação de permissões custom não implementada'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    # Podes estender para PUT, DELETE se quiseres gerir permissões custom
