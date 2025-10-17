"""
Configuración de producción para Huellitas
"""
from .base import *
from dotenv import load_dotenv
load_dotenv()  

# Desactivar Debug en producción
DEBUG = False

# Hosts permitidos en producción
ALLOWED_HOSTS = [
    'localhost',  # Si estás trabajando localmente
    '127.0.0.1',  # Para permitir conexiones locales
    'backend-huellitas-2ft0.onrender.com',  # Agrega tu dominio de Render
    'yourdomain.com',  # Si tienes un dominio personalizado
    'https://proyectohuellitas1.netlify.app/',  # Si tienes un dominio personalizado
]

# Base de datos MySQL para producción
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
                'ca': os.path.join(os.path.dirname(__file__), 'ca.pem'),  # Ruta al archivo ca.pem
            },
        },
    }
}

# Configuración para correos electrónicos en producción (SMTP con SendGrid)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'  # O el servidor SMTP que utilices
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')  # Debes agregar la variable en tu entorno de Render
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')  # Debes agregar la variable en tu entorno de Render
DEFAULT_FROM_EMAIL = 'webmaster@yourdomain.com'  # Cambia este correo según sea necesario

# Configuración CORS más restrictiva en producción
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://proyectohuellitas1.netlify.app",  # Tu dominio frontend
    "https://yourdomain.com",  # Otro dominio autorizado
]

# Configuración de archivos estáticos y de medios
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directorio donde se recopilan los archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio para los archivos de medios (carga de imágenes, documentos, etc.)

# Asegúrate de que las migraciones se apliquen antes de iniciar el servidor en producción
# Puedes hacer esto en el script de despliegue (como `start.sh`) o en el proceso de inicio en Render

# Validación de contraseñas
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

# Internacionalización y zona horaria
LANGUAGE_CODE = 'es-gt'  # Español de Guatemala
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = False

# Configuración de los archivos estáticos y de media
# Esto es necesario para que Django recoja los archivos estáticos cuando se despliegue
# Si tu aplicación está sirviendo archivos estáticos a través de un servidor separado (nginx, AWS S3, etc.), puedes omitir esta parte.
# En Render, asegúrate de que los archivos estáticos y de medios estén disponibles para ser servidos.

# Seguridad adicional en producción
SECURE_SSL_REDIRECT = True  # Redirigir todo el tráfico a HTTPS
SECURE_HSTS_SECONDS = 31536000  # Activar HTTP Strict Transport Security (HSTS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'  # Para evitar clickjacking

# Servir archivos de media y estáticos en producción (en caso de no usar un servidor externo)
# Si usas almacenamiento externo como AWS S3, deberías configurar eso en lugar de esta parte.
if not DEBUG:
    # Asegurarse de servir archivos de media y estáticos correctamente en producción
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Otras configuraciones de seguridad
CSRF_COOKIE_SECURE = True  # Asegúrate de que las cookies CSRF solo se envíen a través de HTTPS
SESSION_COOKIE_SECURE = True  # Asegúrate de que las cookies de sesión solo se envíen a través de HTTPS

# Aplicaciones de Django
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Otras configuraciones adicionales
INTERNAL_IPS = [
    '127.0.0.1',  # Solo para permitir acceso a la consola interna si es necesario
    'localhost',
]

# Otras configuraciones de seguridad
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
