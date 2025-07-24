from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Cria um superusuário automaticamente se ele ainda não existir"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = "Samuel"
        email = "bayala@bayala.co.mz"
        password = "Bayala2025"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.'))
        else:
            self.stdout.write(f'O superusuário "{username}" já existe.')
