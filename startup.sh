#!/bin/bash

echo "Ativando ambiente virtual..."
# No Render, o ambiente virtual geralmente já é usado. Se necessário, descomente:
# source ./venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Removendo usuários duplicados 'Samuel' e criando superusuário se necessário..."
python - <<END
import django
import os
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
END

echo "Iniciando servidor..."
gunicorn bayala_backend.wsgi:application --bind 0.0.0.0:$PORT
