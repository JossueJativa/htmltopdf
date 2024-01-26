from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece la configuración de Django para Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')

# Crea una instancia de la aplicación Celery y configúrala mediante tu configuración de Django.
app = Celery('tu_proyecto')

# Lee la configuración de Django para Celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga las tareas de Celery de todas las aplicaciones de Django.
app.autodiscover_tasks()
