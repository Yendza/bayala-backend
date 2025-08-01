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

# Roda migrações e cria/atualiza superusuário no startup (Render)
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

        # Criar ou atualizar superusuário
        User = get_user_model()
        username = 'Samuel'
        email = 'bayala@bayala.com'
        password = 'Bayala2025'

        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'is_superuser': True,
            'is_staff': True,
        })

        user.set_password(password)  # Atualiza a senha mesmo se o user já existir
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.save()

        if created:
            print("Superusuário admin criado.")
        else:
            print("Superusuário admin já existia. Senha atualizada.")
    except Exception as e:
        print(f"Erro durante as tarefas de inicialização: {e}")

run_startup_tasks()
