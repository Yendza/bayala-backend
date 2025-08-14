# core/management/commands/create_default_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria superusuário padrão se não existir'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='Samuel').exists():
            User.objects.create_superuser(
                username='Samuel',
                email='bayala@bayala.com',
                password='Bayala2025'
            )
            self.stdout.write(self.style.SUCCESS('Superuser criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser já existe.'))
