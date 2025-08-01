"""
WSGI config for bayala_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bayala_backend.settings')

application = get_wsgi_application()

# Roda migrações e cria superusuário no startup (Render)
def run_startup_tasks():
    try:
        import django
        from django.core.management import call_command
        from django.contrib.auth import get_user_model

        django.setup()

        # Aplicar migrações
        print("Aplicando migrações...")
        call_command('migrate', interactive=False)
        print("Migrações concluídas.")

        # Criar superusuário, se não existir
        User = get_user_model()
        username = 'Samuel'
        email = 'bayala@bayala.com'
        password = 'Bayala2025'

        if not User.objects.filter(username=username).exists():
            print("Criando superusuário admin...")
            User.objects.create_superuser(username, email, password)
        else:
            print("Superusuário admin já existe.")
    except Exception as e:
        print(f"Erro durante as tarefas de inicialização: {e}")

run_startup_tasks()
