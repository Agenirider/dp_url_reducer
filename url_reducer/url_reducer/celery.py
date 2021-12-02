import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_reducer.settings')

app = Celery('url_reducer')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_old_urls': {
        'task': 'reducer.tasks.clear_old_urls',
        'schedule': crontab(hour="7,14,21", minute="0")
    },
}