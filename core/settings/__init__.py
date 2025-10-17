"""
Configuración de settings por entorno
"""
import os

# Por defecto usa development, pero puede cambiar con variable de entorno
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .testing import *
else:
    from .development import *