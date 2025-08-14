Write-Host "Ativando ambiente virtual..."
& .\env\Scripts\Activate.ps1  # ajuste aqui para o nome correto do seu env

Write-Host "Instalando dependências..."
pip install -r requirements.txt

Write-Host "Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate --noinput

Write-Host "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

Write-Host "Criando superusuário 'Samuel'..."
python create_superuser.py

Write-Host "Iniciando servidor local..."
python manage.py runserver
