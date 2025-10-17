from .base import *
from dotenv import load_dotenv
load_dotenv()  

# Desactivar Debug en producción
DEBUG = False

# Hosts permitidos en producción
ALLOWED_HOSTS = [
    'localhost',  
    '127.0.0.1',  
    'backend-huellitas-2ft0.onrender.com',  
    'yourdomain.com',
    'https://proyectohuellitas1.netlify.app/',
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
                'ca': os.path.join(os.path.dirname(__file__), 'ca.pem'),  
            },
        },
    }
}

# Configuración de correos electrónicos en producción (SMTP con SendGrid)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')  
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')  
DEFAULT_FROM_EMAIL = 'webmaster@yourdomain.com'

# CORS en producción
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://proyectohuellitas1.netlify.app",  
    "https://yourdomain.com",  
]

# Configuración de archivos estáticos y de medios
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  

# Asegúrate de que las migraciones se apliquen antes de iniciar el servidor en producción

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
LANGUAGE_CODE = 'es-gt'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = False

# Seguridad adicional en producción
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'  

# Servir archivos estáticos y de medios en producción (si no usas un servidor externo)
if not DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Otras configuraciones de seguridad
CSRF_COOKIE_SECURE = True  
SESSION_COOKIE_SECURE = True  

# Otras configuraciones
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
