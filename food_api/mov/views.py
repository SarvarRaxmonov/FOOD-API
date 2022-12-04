from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from mov.models import User_Hardoim_Yeydigan_Foodlari, User_bugun_yegan_foodlari
from django.http import Http404
from mov.serializers import (
    User_Hardoim_Yeydigan_Foodlari_Serializers,
    User_bugun_yegan_foodlari,
    User_bugun_yegan_foodlari_serializer,
    Maslahat_to_User,
    UV,
)
from rest_framework.negotiation import BaseContentNegotiation   
from .permissions import OnlyPersonalUserPermision
from rest_framework.pagination import PageNumberPagination



# Create your views here.

def get_object(element, pk):

    try:
        return element.objects.get(id=pk)
    except element.DoesNotExist:
        raise Http404


class StandartPageSize(APIView, PageNumberPagination):
    page_size = 2
    page_size_query_param = "page-size"
    max_page_size = 2


class User_Hardoim_Yeydigan_Foodlari_View(APIView):

    """
    Salom Bu viewset orqali siz har kuni yeydigan ovqatlar va qancha
    kaloriya yig'ish malumotlarini olishingiz mumkin va o'zgartira olasiz
    """

    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = [IsAuthenticated, OnlyPersonalUserPermision]
    serializer_class = User_Hardoim_Yeydigan_Foodlari_Serializers
    pagination_class = StandartPageSize
    throttle_scope = "ap"

    def get(self, request, id=None):

        if id != None:
            instance = get_object(User_Hardoim_Yeydigan_Foodlari, id)
            self.check_object_permissions(self.request, instance)
            return Response(
                {
                    "Sizning harkunlik taomnomangiz": User_Hardoim_Yeydigan_Foodlari_Serializers(
                        instance, context={"request": request}
                    ).data      
                }
            )

        if request.user.is_staff:
            instance = User_Hardoim_Yeydigan_Foodlari.objects.all()
            return Response(
                User_Hardoim_Yeydigan_Foodlari_Serializers(
                    instance, many=True, context={"request": request}
                ).data
            )

        instance = User_Hardoim_Yeydigan_Foodlari.objects.filter(user=request.user)
        return Response(
            User_Hardoim_Yeydigan_Foodlari_Serializers(
                instance=instance, many=True, context={"request": request}
            ).data
        )

    def put(self, request, id=None):
        
        queryset = User_Hardoim_Yeydigan_Foodlari_Serializers(
            data=request.data,
            instance=User_Hardoim_Yeydigan_Foodlari(),
            context={"user": request.user},
            partial= True
        )
        if queryset.is_valid():
            queryset.save()
        return Response(
            {
                "postlar": queryset.validated_data,
                "Is valid data": queryset.is_valid(),
                "data": request.data,
                "data errors": queryset.errors,
            }
        )

    @classmethod
    def get_extra_actions(cls):
        return []


class User_bugun_yegan_foodlari_View(APIView):
    queryset = User_bugun_yegan_foodlari()
    permission_classes = [IsAuthenticated, OnlyPersonalUserPermision]
    serializer_class = User_bugun_yegan_foodlari_serializer
    pagination_class = [StandartPageSize]

    def get(self, request, id_si=None):
        queryset = User_bugun_yegan_foodlari.objects.filter(user=request.user)
        if id_si != None:
            queryset_detail = User_bugun_yegan_foodlari.objects.get(id_si=id_si)
            return Response(
                {
                    "ovqat_detail": User_bugun_yegan_foodlari_serializer(
                        queryset_detail, context={"request": request}
                    ).data
                }
            )
        return Response(
            {
                "post": User_bugun_yegan_foodlari_serializer(
                    queryset, many=True, context={"request": request}
                ).data
            }
        )

    def post(self, request, id_si=None):
        data = request.data
        print('...................... :::::::::::::::::::::::',id_si)            
        queryset = User_bugun_yegan_foodlari_serializer(
            data=data, context={"user": request.user}
        )
        queryset.is_valid()
        if queryset.is_valid():
            queryset.save()
            m_t_u = Maslahat_to_User(self)
            return Response(
                {
                    "postlar": queryset.validated_data,
                    "maslahat": m_t_u.advice_to_run(food=queryset.validated_data),
                }
            )

        return Response({"data_errors": queryset.errors})

    def put(self, request, id_si=None):

        data = request.data
        queryset = User_bugun_yegan_foodlari_serializer(
            data=data, instance=User_bugun_yegan_foodlari()
        )
        queryset.is_valid()
        queryset.save()
        return Response(
            {
                "postlar": queryset.validated_data,
                "Is valid data": queryset.is_valid(),
                "data": data,
                "data errors": queryset.errors,
            }
        )

    @classmethod
    def get_extra_actions(cls):
        return []


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"Info": "Sizning accountingiz o'chirildi "})
