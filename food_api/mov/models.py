import uuid
from django.db import models
from .food_info import foods_info, ichimliklar
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from multiselectfield import MultiSelectField
from .validators import User_Daily_foods_validators
from django.utils import timezone
from datetime import timedelta
# Write your models

 
class User_Hardoim_Yeydigan_Foodlari_Abstract(models.Model):

    food_name = MultiSelectField(
        choices=foods_info, max_choices=30, max_length=10, default="None"
    )
    ichimliklar = MultiSelectField(choices=ichimliklar, max_choices=30, default="None")
    Qancha_kaloriya = models.DecimalField(
        max_digits=34, decimal_places=0, default="0", null=True
    )
    user = models.CharField(blank=True, max_length=400, default="None")

    class Meta:
        abstract = True
    
        

Gender = [("Erkak", "Erkak"), ("Ayol", "Ayol")]


class User_Hardoim_Yeydigan_Foodlari(User_Hardoim_Yeydigan_Foodlari_Abstract):
    vazn = models.IntegerField(default=0)

    def __str__(self):
        return str(self.food_name)
    
    class Meta:
        verbose_name = "User_hardoim_food"


class User_bugun_yegan_foodlari(User_Hardoim_Yeydigan_Foodlari_Abstract):
    id_si = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sana = models.DateTimeField(null=True, blank=True)
    Qancha_kaloriya = None

    def __str__(self):

        return self.user

class calories_MET_tech_details_add(models.Model):
    met = models.DecimalField(max_digits=34, decimal_places=0, default="0", null=True)
    major_heading = models.CharField(default="None", max_length=200)
    exercise_definition = models.CharField(default="None", max_length=1000)
 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_receiver(sender, instance=None, created=False, **kwargs):

    if created:
        Token.objects.create(user=instance)
        User_Hardoim_Yeydigan_Foodlari.objects.create(user=instance.username)

@receiver(post_save,sender=User_bugun_yegan_foodlari)
def calorie_updater(sender,instance=None, created=True,**kwargs):
    UV = User_Daily_foods_validators()
    if created:
        assosiy = User_Hardoim_Yeydigan_Foodlari.objects.filter(user=instance.user)
        ummumiy_yangi_kaloriya_yigindisi = UV.food_drinks_exists_validator(
            food_name=instance.food_name, ichimliklar=instance.ichimliklar
        )
        Yangi_qushilgan_kaloriya = (
            assosiy.values("Qancha_kaloriya")[0]["Qancha_kaloriya"]
            + ummumiy_yangi_kaloriya_yigindisi
        )
        assosiy.update(Qancha_kaloriya=Yangi_qushilgan_kaloriya)
        
        
        
          
        