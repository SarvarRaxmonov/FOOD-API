from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import User_Hardoim_Yeydigan_Foodlari


@shared_task(bind=True)
def calories_of_user_profile_updater(a=1, b=1):
    User_Hardoim_Yeydigan_Foodlari.objects.all().update(Qancha_kaloriya="0")
    return "done"
