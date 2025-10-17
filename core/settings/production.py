"""
Configuración de producción para Huellitas
"""
import os
from .base import *

# Debug desactivado en producción
DEBUG = False

# Hosts permitidos en producción (configurar según tu dominio)
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Base de datos para producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'huellitas_prod'),
        'USER': os.environ.get('DB_USER', 'huellitas_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')

# Configuración de archivos estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email para producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# CORS más restrictivo en producción
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend.com",
]

# Logging para producción
LOGGING['handlers']['file']['filename'] = '/var/log/huellitas/huellitas.log'
LOGGING['loggers']['django']['level'] = 'WARNING'