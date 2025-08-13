#!/bin/bash

echo "Ativando ambiente virtual..."
source ./venv/bin/activate  # ajuste se seu virtualenv estiver em outro caminho

echo "Atualizando pip e instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Removendo usuários duplicados 'Samuel', mantendo apenas um..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

samuel_users = User.objects.filter(username='Samuel')
if samuel_users.count() > 1:
    # Mantém apenas o primeiro, apaga os demais
    first = samuel_users.first()
    samuel_users.exclude(id=first.id).delete()
    print(f"Removidos {samuel_users.count() - 1} usuários duplicados 'Samuel'.")
else:
    print("Nenhum usuário duplicado 'Samuel' encontrado.")

# Garantir que exista um superusuário Samuel
if not User.objects.filter(username='Samuel').exists():
    User.objects.create_superuser('Samuel', 'bayala@bayala.com', 'Bayala2025')
    print("Superusuário 'Samuel' criado.")
else:
    print("Superusuário 'Samuel' já existe. Nenhuma ação necessária.")
END

echo "Iniciando servidor..."
gunicorn bayala_backend.wsgi:application --bind 0.0.0.0:$PORT
