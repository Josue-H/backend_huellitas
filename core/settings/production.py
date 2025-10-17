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
        'NAME': os.getenv('DB_NAME', 'defaultdb'),
        'USER': os.getenv('DB_USER', 'avnadmin'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'mysql-187c0b93-proyectohuellitasbd-cc9c.b.aivencloud.com'),
        'PORT': os.getenv('DB_PORT', '13886'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'ssl': {
                'ca': os.path.join(os.path.dirname(__file__), 'ca.pem'),  # Ruta relativa al archivo ca.pem
            },
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