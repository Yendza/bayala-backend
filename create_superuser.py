# create_superuser.py
import os
import django

# Configura o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bayala_backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Remove duplicados
samuel_users = User.objects.filter(username='Samuel')
if samuel_users.count() > 1:
    first = samuel_users.first()
    samuel_users.exclude(id=first.id).delete()
    print(f"Removidos {samuel_users.count() - 1} usuários duplicados 'Samuel'.")
else:
    print("Nenhum usuário duplicado 'Samuel' encontrado.")

# Cria superusuário se não existir
if not User.objects.filter(username='Samuel').exists():
    User.objects.create_superuser('Samuel', 'bayala@bayala.com', 'Bayala2025')
    print("Superusuário 'Samuel' criado com sucesso.")
else:
    print("Superusuário 'Samuel' já existe. Nenhuma ação necessária.")
