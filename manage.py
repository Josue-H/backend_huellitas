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
    
    # Asegúrate de que solo modifiques 'runserver' cuando sea necesario
    if 'runserver' in sys.argv:
        # Obtén el puerto desde la variable PORT asignada por Render o 8000 como valor predeterminado
        port = os.getenv('PORT', 8000)
        # Modifica sys.argv para pasar el puerto correctamente
        sys.argv.append(f"0.0.0.0:{port}")  # Ahora se pasa correctamente como argumento al comando
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
