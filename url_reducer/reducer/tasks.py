from datetime import datetime, timedelta

from celery import shared_task
from reducer.models import URLs


@shared_task
def clear_old_urls():
    today = datetime.now()
    month_ago = (today - timedelta(days=30)).date()
    URLs.objects.filter(created_lte=month_ago).delete()
