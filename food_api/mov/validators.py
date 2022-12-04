from rest_framework import serializers
from .food_info import foods_nutrition
import time


def weight_checking_validator(value):
    if value >= 300:
        raise serializers.ValidationError(
            "Afsus bunday vazn calories counter hisoblamaydi "
        )

def new_all_kaloriya_return(*args, **kwargs):
    all_kaloriya = 0

    for food in kwargs.get("dict_food"):
        all_kaloriya += foods_nutrition.get(food)

    return all_kaloriya

def time_converter(mins: int):
    seconds = abs(mins * 60)
    if mins > 60:
        hour = time.localtime(seconds).tm_hour
        minutes = time.localtime(seconds).tm_min
        return f",  {hour} soat {minutes} minut "
    return f",  {int(mins)} minut"


class User_Daily_foods_validators:
    def food_drinks_exists_validator(self, *args, **kwargs):
        all_validated_data = list(kwargs.get("food_name")) + list(
            kwargs.get("ichimliklar")
        )
        for item in all_validated_data:
            if not item in foods_nutrition:
                raise serializers.ValidationError(
                    "Uzur Bunday foodlar bizning datada mavjud emas"
                )

        return new_all_kaloriya_return(dict_food=all_validated_data)

