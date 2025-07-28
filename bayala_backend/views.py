# bayala_backend/views.py

import os
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

def restore_database(request):
    SECRET_KEY = request.GET.get("secret")
    if SECRET_KEY != "restaurar123":
        return HttpResponseForbidden("Chave secreta inválida")

    dump_file = os.path.join(settings.BASE_DIR, "scripts", "bayala_dump.sql")

    command = f'psql -h {settings.DATABASES["default"]["HOST"]} ' \
              f'-U {settings.DATABASES["default"]["USER"]} ' \
              f'-d {settings.DATABASES["default"]["NAME"]} ' \
              f'-p {settings.DATABASES["default"].get("PORT", 5432)} ' \
              f'< "{dump_file}"'

    result = os.system(command)
    if result == 0:
        return HttpResponse("Base de dados restaurada com sucesso!")
    else:
        return HttpResponse("Erro ao restaurar base de dados.")
