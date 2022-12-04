from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foods.settings")
app = Celery("foods")
app.config_from_object(settings, namespace="CELERY")
app.loader.override_backends[
    "django-db"
] = "django_celery_results.backends.database:DatabaseBackend"

app.conf.beat_schedule = {
    "calories": {
        "task": "mov.tasks.calories_of_user_profile_updater",
        "schedule": crontab(hour=14, minute=26),
    }
}


app.autodiscover_tasks()


# to run : celery -A foods beat -l INFO
# to accept task : celery -A foods worker --pool=solo -l info

