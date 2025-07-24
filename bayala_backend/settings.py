from pathlib import Path
import os
from datetime import timedelta
from decouple import config
import dj_database_url


# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django (não compartilhe em produção)
SECRET_KEY = config('SECRET_KEY')

# Modo de depuração (desativar em produção)
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Nome da empresa e logo para o cabeçalho do Django Admin
ADMIN_SITE_HEADER = 'Bayala'  # Nome da empresa
ADMIN_SITE_LOGO = '/media/logos/logo_bayala.png'  # Caminho do logotipo (ajuste o caminho conforme necessário)

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'produtos',
    'clientes',
    'transaccoes',
    'stock',
    'cotacoes',
    'relatorios',
    'configuracoes',
    'corsheaders',
    'django_extensions',
    'usuarios',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3650),  # 10 anos
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3650), # 10 anos
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# Middlewares do Django
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# Para desenvolvimento
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Configurações do URL do projeto
ROOT_URLCONF = 'bayala_backend.urls'

# Configurações de template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Pasta de templates do projeto
        ],
        'APP_DIRS': True,  # Permite procurar templates dentro dos aplicativos
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do WSGI
WSGI_APPLICATION = 'bayala_backend.wsgi.application'

# Configurações do banco de dados (SQLite)
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}




# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalização e localização
LANGUAGE_CODE = 'pt'
TIME_ZONE = 'Africa/Maputo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LANGUAGES = [
    ('pt', 'Português'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Africa/Maputo'

USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH = True

# Configurações de arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configurações padrão de ID de campo
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # frontend local
    "http://127.0.0.1:3000",
    'http://bayalastock.vercel.app',
]
