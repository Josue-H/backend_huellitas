#!/bin/bash

# Ejecutar collectstatic
python manage.py collectstatic --noinput

# Iniciar Gunicorn (o cualquier otro servidor WSGI)
gunicorn core.wsgi:application
