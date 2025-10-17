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
    
    # Modifica esta línea para escuchar en un puerto fijo, por ejemplo el 8000.
    if 'runserver' in sys.argv:
        # Fija el puerto a 8000, o cualquier puerto que desees
        sys.argv.append('0.0.0.0:8000')  # Escuchar en todas las interfaces en el puerto 8000
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
