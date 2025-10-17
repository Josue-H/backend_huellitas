"""
Configuración de desarrollo para Huellitas
"""
from .base import *

# Debug activado en desarrollo
DEBUG = True

# Hosts permitidos en desarrollo
ALLOWED_HOSTS = [
    'localhost',  # Si estás trabajando localmente
    '127.0.0.1',  # Para permitir conexiones locales
    'backend-huellitas-2ft0.onrender.com',  # Agrega tu dominio de Render
    'yourdomain.com',  # Si tienes un dominio personalizado
]

# Base de datos MySQL para desarrollo
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