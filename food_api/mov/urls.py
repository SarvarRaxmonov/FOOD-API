from django.urls import path, include
from rest_framework import routers
from mov.views import User_Hardoim_Yeydigan_Foodlari_View, User_bugun_yegan_foodlari_View, LogOut
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'ap',User_Hardoim_Yeydigan_Foodlari_View, basename='ap')

urlpatterns = [  
    path('', include(router.urls)),
    path('profile', User_Hardoim_Yeydigan_Foodlari_View.as_view(), name='profile') ,
    path('profile/<id>/', User_Hardoim_Yeydigan_Foodlari_View.as_view(), name='profile-detail'),
    path('daily_food/',User_bugun_yegan_foodlari_View.as_view(),name='daily_food'),
    path('daily_food/<id_si>/', User_bugun_yegan_foodlari_View.as_view(),name='daily_food-detail'),
    path('token/',TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/',LogOut.as_view(),name='logout')
 ]



 