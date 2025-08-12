#!/bin/bash
echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Criando superusuário..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="Samuel").exists():
    User.objects.create_superuser("Samuel", "bayala@bayala.com", "Bayala2025")
END

echo "Iniciando servidor..."
gunicorn bayala_backend.wsgi:application --bind 0.0.0.0:$PORT
