"""
Configuración de desarrollo para Huellitas
"""
from .base import *

# Debug activado en desarrollo
DEBUG = True

# Hosts permitidos en desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.1.*']

# Base de datos MySQL para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'defaultdb'),  # Cargar desde la variable DB_NAME
        'USER': os.getenv('DB_USER', 'avnadmin'),  # Cargar desde la variable DB_USER
        'PASSWORD': os.getenv('DB_PASSWORD', ''),  # Cargar desde la variable DB_PASSWORD
        'HOST': os.getenv('DB_HOST', 'mysql-187c0b93-proyectohuellitasbd-cc9c.b.aivencloud.com'),  # Cargar desde DB_HOST
        'PORT': os.getenv('DB_PORT', '13886'),  # Cargar desde DB_PORT
        'OPTIONS': {
            'ssl': {'ca': '/path/to/ca.pem'},  # Si estás usando SSL
            'use_pure': True  # Asegurarse de que esté usando el conector de MySQLX
        },
    }
}

# Email para desarrollo (aparece en consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS más permisivo en desarrollo
CORS_ALLOW_ALL_ORIGINS = True

# Configuraciones adicionales para desarrollo
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Django Extensions si se instala
try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass