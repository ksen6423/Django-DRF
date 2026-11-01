from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery


from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Используем настройки Django для Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в файлах tasks.py
app.autodiscover_tasks()

# Настройка timezone, если она не установлена в settings.py
# Убедитесь, что USE_TZ = True в ваших настройках Django
if settings.USE_TZ:
    timezone.activate(settings.TIME_ZONE)
