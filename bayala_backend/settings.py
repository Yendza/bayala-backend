from pathlib import Path
import os
import re
from datetime import timedelta
from decouple import config
import dj_database_url

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django
SECRET_KEY = config('SECRET_KEY')

# Debug mode
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = [
    "bayala-backend-5.onrender.com",  # Backend no Render
    "localhost",
    "127.0.0.1",
    "bayalastock.vercel.app",         # Produção no Vercel
    "https://bayala-frontend-yendzas-projects.vercel.app",
    "bayala-frontend-git-main-yendzas-projects.vercel.app",
    "bayala-frontend-djie8qp6c-yendzas-projects.vercel.app",
]
# Aceitar qualquer subdomínio de vercel.app (previews)
ALLOWED_HOSTS_REGEX = re.compile(r"^.*\.vercel\.app$")

# Detecta se está em produção
RENDER = config('RENDER', default=False, cast=bool)

# Configuração do banco de dados
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', cast=int),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

# Logo e nome no Admin
ADMIN_SITE_HEADER = 'Bayala'
ADMIN_SITE_LOGO = '/media/logos/logo_bayala.png'

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

    'corsheaders',
    'django_extensions',

    # Seus apps
    'produtos',
    'clientes',
    'transaccoes',
    'stock',
    'cotacoes',
    'relatorios',
    'configuracoes',
    'usuarios',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # TEM que ser o primeiro
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3650),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3650),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Segurança
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# CORS
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Só libera tudo em debug
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://bayalastock.vercel.app',  # Produção
    'https://bayala-frontend-yendzas-projects.vercel.app',
    'bayala-frontend-git-main-yendzas-projects.vercel.app',
    'bayala-frontend-djie8qp6c-yendzas-projects.vercel.app',
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/.*\.vercel\.app$",  # Previews Vercel
]

# Templates
ROOT_URLCONF = 'bayala_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'bayala_backend.wsgi.application'

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt'
LANGUAGES = [('pt', 'Português')]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
TIME_ZONE = 'Africa/Maputo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Django padrão para chaves primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = True
