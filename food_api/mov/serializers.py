from dataclasses import dataclass
from django.utils import timezone
from rest_framework import serializers
from .food_info import foods_info, ichimliklar
from .models import (
    User_bugun_yegan_foodlari,
    User_Hardoim_Yeydigan_Foodlari,
    calories_MET_tech_details_add,
)
from .validators import (
    weight_checking_validator,
    User_Daily_foods_validators,
    time_converter,
)

UV = User_Daily_foods_validators()


class User_Hardoim_Yeydigan_Foodlari_Serializers(serializers.Serializer):

    Qancha_kaloriya = serializers.DecimalField(
        max_digits=34, decimal_places=0, default=12, read_only=True  
    )
    food_name = serializers.MultipleChoiceField(choices=foods_info, default="None")
    ichimliklar = serializers.MultipleChoiceField(choices=ichimliklar, default="None")
    user = serializers.CharField(read_only=True)
    update_qilish_uchun = serializers.HyperlinkedIdentityField(
        view_name="profile-detail", lookup_field="id"
    )
    vazn = serializers.IntegerField(validators=[weight_checking_validator], required = False )

    class Meta:
        model = User_Hardoim_Yeydigan_Foodlari
        fields = (
            "user",
            "Qancha_kaloriya",
            "food_name",
            "Ichimliklar",
            "vazn",
            "update_qilish_uchun",
        )
        extra_kwargs = {
            "food_name": {
                "error_messages": {
                    "invalid": "Please Enter Valid Name.",
                    "required": "Please Enter Full Name.",
                }
            },
        }

    def update(self, instance, validated_data):
        return User_Hardoim_Yeydigan_Foodlari.objects.filter(
            user=self.context.get("user")
        ).update(**validated_data)


class User_bugun_yegan_foodlari_serializer(serializers.ModelSerializer):

    food_name = serializers.MultipleChoiceField(choices=foods_info, default="None")
    ichimliklar = serializers.MultipleChoiceField(choices=ichimliklar, default="None")
    sana = serializers.HiddenField(default=timezone.now)

    class Meta:

        model = User_bugun_yegan_foodlari
        fields = ("food_name", "ichimliklar", "url", "sana", "id_si")

        extra_kwargs = {
            "url": {"view_name": "daily_food-detail", "lookup_field": "id_si"},
            "sana": {"format": "iso-8601"},
        }

    def create(self, validated_data):
        
        return User_bugun_yegan_foodlari.objects.create(
            **validated_data, user=self.context.get("user")
        ) 


@dataclass
class Maslahat_to_User:
    dicts: dict

    def advice_to_run(self, food=None):
        main_dict = {}
        counter = UV.food_drinks_exists_validator(
            food_name=food["food_name"], ichimliklar=food["ichimliklar"]
        )
        right_met = self.get_right_met(calories=counter)
        cv = calories_MET_tech_details_add.objects.filter(met__lte=right_met).order_by(
            "?"
        )
        for i in cv:
            count_time_of_doing_exercise = abs(counter / (int(i.met) * 3.5 * 73 / 200))
            main_dict[i.major_heading] = i.exercise_definition + time_converter(
                count_time_of_doing_exercise
            )
        return main_dict

    def get_right_met(self, calories: int = 0):
        met_level = [
            [0, [10]],
            [3, [100]],
            [5, [400]],
            [8, [800]],
            [11, [1100]],
            [15, [2700]],
        ]
        met = 0
        if isinstance(calories, int) and calories < 3000:
            for met in range(len(met_level) - 1):
                if (
                    calories > met_level[met][1][0]
                    and calories < met_level[met + 1][1][0]
                ):
                    met = met_level[met + 1][0]
                    break
                continue
        else:
            raise serializers.ValidationError(
                "Uzur buncha calories hisoblash iloji yuq sog'lig'ingizga zarar"
            )
        return met
