"""
Configuración para tests de Huellitas
"""
from .base import *

# Debug activado para tests
DEBUG = True

# Base de datos en memoria para tests (más rápido)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Email para tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Desactivar migraciones en tests (más rápido)
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Password hashers más rápidos para tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Logging mínimo para tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}