#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Asegurarse de que si se está ejecutando runserver, el puerto se pase correctamente
    if 'runserver' in sys.argv:
        # Se añade 0.0.0.0:8000 o el puerto asignado por Render si está disponible
        sys.argv.append(f"0.0.0.0:{os.getenv('PORT', 8000)}")  # Usa el puerto proporcionado por Render, o 8000 por defecto
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
