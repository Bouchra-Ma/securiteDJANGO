# securite/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securite.settings')

app = Celery('securite')

# Chargement des settings Django pour Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tasks dans chaque app
app.autodiscover_tasks()

