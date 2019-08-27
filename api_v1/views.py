from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication
from api_v1.serializers import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import random
import string
from datetime import datetime
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils.decorators import method_decorator
from rest_framework.authentication import *
from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class UserViews(APIView):
    """
    Представление пользователя
    """
    permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        profile = Profile.objects.get(client=request.user)
        manager = Profile.objects.get(meneger=profile.meneger)
        man = Profile.objects.filter()
        listObjects = []
        for managerobject in man:
            if managerobject.id == manager.meneger:
                #print(managerobject)
                name_manage = managerobject
                listObjects.append(managerobject)
                print(managerobject.client.first_name)
                phone = managerobject.client.username
                print(phone)
                email = managerobject.client.email
            #print(managerobject.id)

        print('=',manager.meneger)

        serializer = profileSerializer(profile)

        return JsonResponse(
            {"data":serializer,"manager":{"name":managerobject.client.first_name,"email":email,"phone":phone}}
        )
class ObjectsPropertyOwnerViews(APIView):
    """
    Представление для объектов недвижимости в
    собственности пользователя
    """
    permission_classes = [permissions.IsAuthenticated]

    #http_method_names = ['POST']
    #queryset = EstateObject.objects.all()
    #serializer_class = objectPropertySerializer
    #pagination_class = None


    def post(self,request):

        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            listEstateObjects = EstateObject.objects.filter(owner=profile.id)

            listObjects = []
            for estateObject in listEstateObjects:
                print(estateObject.pk)
                listObjects.append(objectPropertySerializer_1(estateObject,True))
            return JsonResponse({'data':{'listObjects':listObjects}})
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Собственник'})
            response.status_code = 403
            return response

class OneObjectPropertyOwnerViews(APIView):
    """
    Представление для конкретного объекта недвижимости в
    собственности пользователя
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            try:
                selectObject = EstateObject.objects.get(id=request.POST['id'])
                print(selectObject.id)
                ss = EstateObject.objects.filter(id=request.POST['id'])
                print(ss)
                return JsonResponse({'data':objectPropertySerializer_1(selectObject)})
            except BaseException:
                response = JsonResponse({'data':'Объект недвижимости с таким id не найден'})
                response.status_code = 404
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Собственник'})
            response.status_code = 403
            return response

import json

class EmploymentNowViews(APIView):
    """
    Представление для проверки занятости площади в данный момент
    для определённого объекта нидвижимости
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            a = []
            selectObject = EstateObject.objects.get(id=request.POST['id'])
            contractObject = Contract.objects.filter(estateObject=selectObject)

            a = areaSerialivers(contractObject)

            area = selectObject.area

            #proc = a/area
            #proc *= 100


            #if selectObject.getBusyArea():
            #    return JsonResponse({'data': selectObject.getBusyArea()})
            #elif selectObject.getVacantArea():
            return JsonResponse({'data':a,'total_area': selectObject.area})
        else:
            response = JsonResponse({'data': 'Нет доступа'})
            response.status_code = 403
            return response

class EmploymentOverPeriodViews(APIView):
    """
    Представление для проверки занятости площади за период
    для определённого объекта нидвижимости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)

        if profile.isOwner():
            selectObject = EstateObject.objects.get(id=request.POST['id'])


            if selectObject.getBusyArea():
                statusdata = []
                alls = []
                date_contract = []
                ex_date = []

                selectPeriod_1 = request.POST['period']
                selectPeriod = Contract.objects.filter(estateObject=selectObject)

                for periods in selectPeriod:
                    statusdata.append(periods)
                    if selectPeriod_1 == '3':
                        #print(i)
                        areas = 0
                        if periods.dateContract.month >= 1: #and periods.dateContract.month <= periods.expirationDateContract.month:
                            if periods.expirationDateContract.month <= 12:
                                if periods.dateContract.month <= 1 and periods.expirationDateContract.month >=1:
                                    one_1 = True
                                    areas_1 = periods.area
                                    free_1 = periods.estateObject.area - periods.area
                                    year_1 = periods.dateContract.year
                                else:
                                    one_1 = False
                                    areas_1 = 0
                                    free_1 = periods.estateObject.area
                                    year_1 = periods.dateContract.year
                                if periods.dateContract.month <= 2 and periods.expirationDateContract.month >=2:
                                    one_2 = True
                                    areas_2 = periods.area
                                    free_2 = periods.estateObject.area - periods.area
                                    year_2 = periods.dateContract.year
                                else:
                                    one_2 = False
                                    areas_2 = 0
                                    free_2 = periods.estateObject.area
                                    year_2 = periods.dateContract.year
                                if periods.dateContract.month  <= 3 and periods.expirationDateContract.month >=3:
                                    one_3 = True
                                    areas_3 = periods.area
                                    free_3 = periods.estateObject.area - periods.area
                                    year_3 = periods.dateContract.year
                                else:
                                    one_3 = False
                                    areas_3 = areas
                                    free_3 = periods.estateObject.area
                                    year_3 = periods.dateContract.year
                                return JsonResponse({'data': [{'employment':one_1, 'month':'Январь', 'area':areas_1, 'free':free_1, 'year': year_1}, {'employment':one_2, 'month':'Февраль', 'area':areas_2, 'free':free_2, 'year': year_2}, {'employment':one_3, 'month':'Март', 'area':areas_3, 'free':free_3, 'year': year_3}]})

                    elif selectPeriod_1 == '6':
                        if periods.dateContract.month >= 1: #and periods.dateContract.month <= periods.expirationDateContract.month:
                            if periods.expirationDateContract.month <= 12:
                                if periods.dateContract.month <= 1 and periods.expirationDateContract.month >=1:
                                    two_1 = True
                                    areas_1 = periods.area
                                    free_1 = periods.estateObject.area - periods.area
                                    year_1 = periods.dateContract.year
                                else:
                                    two_1 = False
                                    areas_1 = 0
                                    free_1 = periods.estateObject.area
                                    year_1 = periods.dateContract.year
                                if periods.dateContract.month <= 2 and periods.expirationDateContract.month >=2:
                                    two_2 = True
                                    areas_2 = periods.area
                                    free_2 = periods.estateObject.area - periods.area
                                    year_2 = periods.dateContract.year
                                else:
                                    two_2 = False
                                    areas_2 = 0
                                    free_2 = periods.estateObject.area
                                    year_2 = periods.dateContract.year
                                if periods.dateContract.month <= 3 and periods.expirationDateContract.month >=3:
                                    two_3 = True
                                    areas_3 = periods.area
                                    free_3 = periods.estateObject.area - periods.area
                                    year_3 = periods.dateContract.year
                                else:
                                    two_3 = False
                                    areas_3 = 0
                                    free_3 = periods.estateObject.area
                                    year_3 = periods.dateContract.year
                                if periods.dateContract.month <= 4 and periods.expirationDateContract.month >=4:
                                    two_4 = True
                                    areas_4 = periods.area
                                    free_4 = periods.estateObject.area - periods.area
                                    year_4 = periods.dateContract.year
                                else:
                                    two_4 = False
                                    areas_4 = 0
                                    free_4 = periods.estateObject.area
                                    year_4 = periods.dateContract.year
                                if periods.dateContract.month <= 5 and periods.expirationDateContract.month >=5:
                                    two_5 = True
                                    areas_5 = periods.area
                                    free_5 = periods.estateObject.area - periods.area
                                    year_5 = periods.dateContract.year
                                else:
                                    two_5 = False
                                    areas_5 = 0
                                    free_5 = periods.estateObject.area
                                    year_5 = periods.dateContract.year
                                if periods.dateContract.month <= 6 and periods.expirationDateContract.month >=6:
                                    two_6 = True
                                    areas_6 = periods.area
                                    free_6 = periods.estateObject.area - periods.area
                                    year_6 = periods.dateContract.year
                                else:
                                    two_6 = False
                                    areas_6 = 0
                                    free_6 = periods.estateObject.area
                                    year_6 = periods.dateContract.year
                                return JsonResponse({'data': [{'employment':two_1, 'month':'Январь', 'area':areas_1, 'free':free_1, 'year': year_1}, {'employment':two_2, 'month':'Февраль', 'area':areas_2, 'free':free_2, 'year': year_2}, {'employment':two_3, 'month':'Март', 'area':areas_3, 'free':free_3, 'year': year_3}, {'employment':two_4, 'month':'Апрель', 'area':areas_4, 'free':free_4, 'year': year_4}, {'employment':two_5, 'month':'Май', 'area':areas_5, 'free':free_5, 'year': year_5}, {'employment':two_6, 'month':'Июнь', 'area':areas_6, 'free':free_6, 'year': year_6}]})

                    elif selectPeriod_1 == '9':
                        if periods.dateContract.month >= 1: #and periods.dateContract.month <= periods.expirationDateContract.month:
                            if periods.expirationDateContract.month <= 12:
                                if periods.dateContract.month <= 1 and periods.expirationDateContract.month >=1:
                                    two_1 = True
                                    areas_1 = periods.area
                                    free_1 = periods.estateObject.area - periods.area
                                    year_1 = periods.dateContract.year
                                else:
                                    two_1 = False
                                    areas_1 = 0
                                    free_1 = periods.estateObject.area
                                    year_1 = periods.dateContract.year
                                if periods.dateContract.month <= 2 and periods.expirationDateContract.month >=2:
                                    two_2 = True
                                    areas_2 = periods.area
                                    free_2 = periods.estateObject.area - periods.area
                                    year_2 = periods.dateContract.year
                                else:
                                    two_2 = False
                                    areas_2 = 0
                                    free_2 = periods.estateObject.area
                                    year_2 = periods.dateContract.year
                                if periods.dateContract.month <= 3 and periods.expirationDateContract.month >=3:
                                    two_3 = True
                                    areas_3 = periods.area
                                    free_3 = periods.estateObject.area - periods.area
                                    year_3 = periods.dateContract.year
                                else:
                                    two_3 = False
                                    areas_3 = 0
                                    free_3 = periods.estateObject.area
                                    year_3 = periods.dateContract.year
                                if periods.dateContract.month <= 4 and periods.expirationDateContract.month >=4:
                                    two_4 = True
                                    areas_4 = periods.area
                                    free_4 = periods.estateObject.area - periods.area
                                    year_4 = periods.dateContract.year
                                else:
                                    two_4 = False
                                    areas_4 = 0
                                    free_4 = periods.estateObject.area
                                    year_4 = periods.dateContract.year
                                if periods.dateContract.month <= 5 and periods.expirationDateContract.month >=5:
                                    two_5 = True
                                    areas_5 = periods.area
                                    free_5 = periods.estateObject.area - periods.area
                                    year_5 = periods.dateContract.year
                                else:
                                    two_5 = False
                                    areas_5 = 0
                                    free_5 = periods.estateObject.area
                                    year_5 = periods.dateContract.year
                                if periods.dateContract.month <= 6 and periods.expirationDateContract.month >=6:
                                    two_6 = True
                                    areas_6 = periods.area
                                    free_6 = periods.estateObject.area - periods.area
                                    year_6 = periods.dateContract.year
                                else:
                                    two_6 = False
                                    areas_6 = 0
                                    free_6 = periods.estateObject.area
                                    year_6 = periods.dateContract.year
                                if periods.dateContract.month <= 7 and periods.expirationDateContract.month >=7:
                                    two_7 = True
                                    areas_7 = periods.area
                                    free_7 = periods.estateObject.area - periods.area
                                    year_7 = periods.dateContract.year
                                else:
                                    two_7 = False
                                    areas_7 = 0
                                    free_7 = periods.estateObject.area
                                    year_7 = periods.dateContract.year
                                if periods.dateContract.month <= 8 and periods.expirationDateContract.month >=8:
                                    two_8 = True
                                    areas_8 = periods.area
                                    free_8 = periods.estateObject.area - periods.area
                                    year_8 = periods.dateContract.year
                                else:
                                    two_8 = False
                                    areas_8 = 0
                                    free_8 = periods.estateObject.area
                                    year_8 = periods.dateContract.year
                                if periods.dateContract.month <= 9 and periods.expirationDateContract.month >=9:
                                    two_9 = True
                                    areas_9 = periods.area
                                    free_9 = periods.estateObject.area - periods.area
                                    year_9 = periods.dateContract.year
                                else:
                                    two_9 = False
                                    areas_9 = 0
                                    free_9 = periods.estateObject.area
                                    year_9 = periods.dateContract.year
                                return JsonResponse({'data': [{'employment':two_1, 'month':'Январь', 'area':areas_1, 'free':free_1, 'year': year_1}, {'employment':two_2, 'month':'Февраль', 'area':areas_2, 'free':free_2, 'year': year_2}, {'employment':two_3, 'month':'Март', 'area':areas_3, 'free':free_3, 'year': year_3}, {'employment':two_4, 'month':'Апрель', 'area':areas_4, 'free':free_4, 'year': year_4}, {'employment':two_5, 'month':'Май', 'area':areas_5, 'free':free_5, 'year': year_5}, {'employment':two_6, 'month':'Июнь', 'area':areas_6, 'free':free_6, 'year': year_6}, {'employment':two_7, 'month':'Июль', 'area':areas_7, 'free':free_7, 'year': year_7}, {'employment':two_8, 'month':'Август', 'area':areas_8, 'free':free_8, 'year': year_8}, {'employment':two_9, 'month':'Сентябрь', 'area':areas_9, 'free':free_9, 'year': year_9}]})

                    if selectPeriod_1 == '12':
                        if periods.dateContract.month >=1 and periods.dateContract.month <= periods.expirationDateContract.month:
                            if periods.expirationDateContract.month <= 12:
                                if periods.dateContract.month <= 1 and periods.expirationDateContract.month >=1:
                                    three_1 = True
                                    areas_1 = periods.area
                                    free_1 = periods.estateObject.area - periods.area
                                    year_1 = periods.dateContract.year
                                else:
                                    three_1 = False
                                    areas_1 = 0
                                    free_1 = periods.estateObject.area
                                    year_1 = periods.dateContract.year
                                if periods.dateContract.month <= 2 and periods.expirationDateContract.month >=2:
                                    three_2 = True
                                    areas_2 = periods.area
                                    free_2 = periods.estateObject.area - periods.area
                                    year_2 = periods.dateContract.year
                                else:
                                    three_2 = False
                                    areas_2 = 0
                                    free_2 = periods.estateObject.area
                                    year_2 = periods.dateContract.year
                                if periods.dateContract.month <= 3 and periods.expirationDateContract.month >=3:
                                    three_3 = True
                                    areas_3 = periods.area
                                    free_3 = periods.estateObject.area - periods.area
                                    year_3 = periods.dateContract.year
                                else:
                                    three_3 = False
                                    areas_3 = 0
                                    free_3 = periods.estateObject.area
                                    year_3 = periods.dateContract.year
                                if periods.dateContract.month <= 4 and periods.expirationDateContract.month >=4:
                                    three_4 = True
                                    areas_4 = periods.area
                                    free_4 = periods.estateObject.area - periods.area
                                    year_4 = periods.dateContract.year
                                else:
                                    three_4 = False
                                    areas_4 = 0
                                    free_4 = periods.estateObject.area
                                    year_4 = periods.dateContract.year
                                if periods.dateContract.month <= 5 and periods.expirationDateContract.month >=5:
                                    three_5 = True
                                    areas_5 = periods.area
                                    free_5 = periods.estateObject.area - periods.area
                                    year_5 = periods.dateContract.year
                                else:
                                    three_5 = False
                                    areas_5 = 0
                                    free_5 = periods.estateObject.area
                                    year_5 = periods.dateContract.year
                                if periods.dateContract.month <= 6 and periods.expirationDateContract.month >=6:
                                    three_6 = True
                                    areas_6 = periods.area
                                    free_6 = periods.estateObject.area - periods.area
                                    year_6 = periods.dateContract.year
                                else:
                                    three_6 = False
                                    areas_6 = 0
                                    free_6 = periods.estateObject.area
                                    year_6 = periods.dateContract.year
                                if periods.dateContract.month <= 7 and periods.expirationDateContract.month >=7:
                                    three_7 = True
                                    areas_7 = periods.area
                                    free_7 = periods.estateObject.area - periods.area
                                    year_7 = periods.dateContract.year
                                else:
                                    three_7 = False
                                    areas_7 = 0
                                    free_7 = periods.estateObject.area
                                    year_7 = periods.dateContract.year
                                if periods.dateContract.month <= 8 and periods.expirationDateContract.month >=8:
                                    three_8 = True
                                    areas_8 = periods.area
                                    free_8 = periods.estateObject.area - periods.area
                                    year_8 = periods.dateContract.year
                                else:
                                    three_8 = False
                                    areas_8 = 0
                                    free_8 = periods.estateObject.area
                                    year_8 = periods.dateContract.year
                                if periods.dateContract.month <= 9 and periods.expirationDateContract.month >=9:
                                    three_9 = True
                                    areas_9 = periods.area
                                    free_9 = periods.estateObject.area - periods.area
                                    year_9 = periods.dateContract.year
                                else:
                                    three_9 = False
                                    areas_9 = 0
                                    free_9 = periods.estateObject.area
                                    year_9 = periods.dateContract.year
                                if periods.dateContract.month <= 10 and periods.expirationDateContract.month >=10:
                                    three_10 = True
                                    areas_10 = periods.area
                                    free_10 = periods.estateObject.area - periods.area
                                    year_10 = periods.dateContract.year
                                else:
                                    three_10 = False
                                    areas_10 = 0
                                    free_10 = periods.estateObject.area
                                    year_10 = periods.dateContract.year
                                if periods.dateContract.month <= 11 and periods.expirationDateContract.month >=11:
                                    three_11 = True
                                    areas_11 = periods.area
                                    free_11 = periods.estateObject.area - periods.area
                                    year_11 = periods.dateContract.year
                                else:
                                    three_11 = False
                                    areas_11 = 0
                                    free_11 = periods.estateObject.area
                                    year_11 = periods.dateContract.year
                                if periods.dateContract.month <= 12 and periods.expirationDateContract.month >=12:
                                    three_12 = True
                                    areas_12 = periods.area
                                    free_12 = periods.estateObject.area - periods.area
                                    year_12 = periods.dateContract.year
                                else:
                                    three_12 = False
                                    areas_12 = 0
                                    free_12 = periods.estateObject.area
                                    year_12 = periods.dateContract.year
                                return JsonResponse({'data': [{'employment':three_1, 'month':'Январь', 'area':areas_1, 'free':free_1, 'year': year_1}, {'employment':three_2, 'month':'Февраль', 'area':areas_2, 'free':free_2, 'year': year_2}, {'employment':three_3, 'month':'Март', 'area':areas_3, 'free':free_3, 'year': year_3}, {'employment':three_4, 'month':'Апрель', 'area':areas_4, 'free':free_4, 'year': year_4}, {'employment':three_5, 'month':'Май', 'area':areas_5, 'free':free_5, 'year': year_5}, {'employment':three_6, 'month':'Июнь', 'area':areas_6, 'free':free_6, 'year': year_6},{'employment':three_7, 'month':'Июль', 'area':areas_7, 'free':free_7, 'year': year_7}, {'employment':three_8, 'month':'Август', 'area':areas_8, 'free':free_8, 'year': year_8}, {'employment':three_9, 'month':'Сентябрь', 'area':areas_9, 'free':free_9, 'year': year_9}, {'employment':three_10, 'month':'Октябрь', 'area':areas_10, 'free':free_10, 'year': year_10}, {'employment':three_11, 'month':'Ноябрь', 'area':areas_11, 'free':free_11, 'year': year_11}, {'employment':three_12, 'month':'Декабрь', 'area':areas_12, 'free':free_12, 'year': year_12}]})
                else:
                    return JsonResponse({'data': 'error'})
            elif selectObject.getVacantArea():
                print('false')

            #except:
            #    return JsonResponse({'data':'error'})
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class ListTenantresViews(APIView):
    """
    Представлени для отображения списка арендаторов для определённого
    объекта нидвижимости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:

            listObjects = []
            listobjec = EstateObject.objects.get(id = request.POST['id'])
            profile = Profile.objects.get(client=request.user)
            clients = Tenantry.objects.filter(estateObject=listobjec)

            for client in clients:
                listObjects.append(ListTenantresViewsSerializer(client,profile))
            return JsonResponse({'data': listObjects})
            #return JsonResponse({'data': ListTenantresViewsSerializer(clients)})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response


class CostNowViews(APIView):
    """
    Представление для проверки издержек объекта в данный момент
    для определённого объекта нидвижимости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            selectEstateObject = EstateObject.objects.get(id=request.POST['id'])
            totalCosts = Cost.objects.filter(estateObject=selectEstateObject)
            cost = ChargeUtilityBills.objects.filter(estateObject=selectEstateObject)
            return JsonResponse({'data':costNowSerializer(totalCosts, cost)})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class CostOverPeriodViews(APIView):
    """
    Представление для проверки издержек объекта за период
    для определённого объекта нидвижимости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            lists_util = []
            list_total = []
            list_cahs = []
            periods = []

            utilss = []
            cashss = []
            cashss_2 = []
            cashss_3 = []
            totalss = []
            selectRealt = EstateObject.objects.get(id=request.POST['id'])
            period = request.POST['period']

            selectPeriod = Cost.objects.filter(estateObject=selectRealt)
            selectUtil = ChargeUtilityBills.objects.filter(estateObject=selectRealt)
            selectTotal = CashFlow.objects.filter(estateObject=selectRealt)


            try:
                if period == '3':
                    for cash in selectPeriod:
                        date_cash = cash.datePayment.month
                        #print('ONE = ', list_cahs)

                    for total in selectTotal:
                        date_total = total.datePayment.month
                        #print('TWO = ', list_total)

                    for util in selectUtil:

                        date_util = util.datePayment.month
                        #print('THREE = ', lists_util)

                    #if date_util <= 3 and date_total <= 3 and date_cash <=3:
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <=3:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <=3:
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 3:

                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                        'total': utilss,
                        'utility_payments': cashss,
                        'operating_cost': totalss,
                        'etc': cashss_2
                    }})

                elif period == '6':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        print('1 - ',ch)
                        if ch <= 6:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        print('2 - ',pr)
                        if pr <= 6:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 6:
                            print('3 - ',ut)
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})

                elif period == '9':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <= 9:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <= 9:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 9:
                            print(ut)
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                        'total': utilss,
                        'utility_payments': cashss,
                        'operating_cost': totalss,
                        'etc': cashss_2
                    }})
                elif period == '12':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <= 12:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <= 12:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 12:
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})
                else:
                    response = JsonResponse({'data': 'Нет доступа'})
                    return response

            except BaseException:
                response = JsonResponse({'data':'Ошибка сервера'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class ListFilesViews(APIView):
    """
    Представлени для отображения списка загруженых файлов
    для определённого объекта нидвижимости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            selectObject = EstateObject.objects.get(id=request.POST['id'])
            files = UploadFile.objects.filter(estateObject=selectObject)
            profileObject = Profile.objects.get(owner_set=selectObject)
            listObjects = []
            for file in files:
                listObjects.append(fileSerializer(file, profileObject))
            return JsonResponse({'data':listObjects})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class ObjectsPropertyTenantViews(APIView):
    """
    Представление для объекта недвижимости
    арендуемой пользователем
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isTenant():
            listEstateObjects = EstateObject.objects.filter(owner = profile.id)
            test = Tenantry.objects.filter(tenantry = profile.id)


            listObjects = []
            for estateObject in test:

                listObjects.append(objectPropertySerializer(estateObject,False))
            return JsonResponse({'data':{'listObjects':listObjects}})
        else:
            response = JsonResponse({'data':'Ошибка доступа'})
            response.status_code = 403
            return response

class OneObjectPropertyTenantViews(APIView):
    """
    Представление для списка объектов недвижимости
    арендуемой пользователем
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isTenant():
            utl_list = []
            ID = request.POST['id']
            test = Tenantry.objects.get(estateObject=ID)
            indications =  MeterReadings.objects.filter(estateObject=test.estateObject)
            utilityPayments = ChargeUtilityBills.objects.filter(estateObject=test.estateObject)
            contract = Contract.objects.get(rent=test.tenantry)
            utl1 = ChargeUtilityBills.objects.filter(estateObject=test.estateObject)
            for utls in utl1:
                utl_list.append(utls)

            for ind in indications:
                pass
            data = objectPropertyForTenantSerializer(
                test.estateObject,
                indications,
                utls,
                utilityPayments,
                contract,
                preview=False
            )
            return JsonResponse({'data':data})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка сервера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Арендатор'})
            response.status_code = 403
            return response



class TotalRentalFlowNowViews(APIView):
    """
    Представления для отображения общей статистики
    арендного потока за год
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            try:
                estateObjects = EstateObject.objects.filter(owner=profile)
                cashFlow = []
                for item in estateObjects:
                    cashFlow += CashFlow.objects.filter(estateObject=item)
                amount = 0
                for item in cashFlow:
                    amount += item.amount
                return JsonResponse({'data':amount})
            except BaseException:
                response = JsonResponse({'data':'Ошибка серрвера'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class TotalRentalFlowOverPeriodViews(APIView):
    """
        Представления для отображения общей статистики
        арендного потока за выбранный период
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            tests = []
            periods = []
            p1 = CashFlow.objects.filter(payer_id=profile)
            estateObjects = EstateObject.objects.filter(owner=profile)
            selectInterlocutor = request.POST['period']
            for item in estateObjects:
                periods += CashFlow.objects.filter(estateObject=item)


            for per in periods:
                if selectInterlocutor == '3':
                    if per.datePayment.month == 1 or per.datePayment.month == 2 or per.datePayment.month == 3:
                        tests.append(mouthSerializer(per))
                elif selectInterlocutor == '6':
                    if per.datePayment.month == 1 or per.datePayment.month == 2 or per.datePayment.month == 3 or per.datePayment.month == 4 or per.datePayment.month == 5 or per.datePayment.month == 6:
                        tests.append(mouthSerializer(per))
                elif selectInterlocutor == '9':
                    if per.datePayment.month == 1 or per.datePayment.month == 2 or per.datePayment.month == 3 or per.datePayment.month == 4 or per.datePayment.month == 5 or per.datePayment.month == 6 or per.datePayment.month == 7 or per.datePayment.month == 8 or per.datePayment.month == 9:
                        tests.append(mouthSerializer(per))
                elif selectInterlocutor == '12':
                    if per.datePayment.month == 1 or per.datePayment.month == 2 or per.datePayment.month == 3 or per.datePayment.month == 4 or per.datePayment.month == 5 or per.datePayment.month == 6 or per.datePayment.month == 7 or per.datePayment.month == 8 or per.datePayment.month == 9 or per.datePayment.month == 10 or per.datePayment.month == 11 or per.datePayment.month == 12:
                        tests.append(mouthSerializer(per))
                else:
                    return JsonResponse({'data': 'Ошибка. period может быть только: 3, 6, 9, 12.'})




            return JsonResponse({'data': tests})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class TotalEmploymentNowViews(APIView):
    """
    Представления для отображения общей статистики
    занятости площади за год
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            selectObject = EstateObject.objects.filter(owner=profile)
            selectPeriod = Contract.objects.filter(rent=profile)

            area = 0
            for periods in selectPeriod:
                print(periods.area)
            areaBusy = profile.getBusyArea_2()
            areaVacant = profile.getVacantArea_2()
            areaTotal = profile.getTotalArea()
            areaTotalS = profile.getTotalAreaSs()
            return JsonResponse({
                'data':areaNowSerializer(areaBusy,areaVacant,areaTotal, areaTotalS)
            })
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class TotalEmploymentOverPeriodViews(APIView):
    """
    Представления для отображения общей статистики
    занятости площади за выбранный период
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            contracts = []
            ids = []
            selectPeriod = request.POST['period']
            estateObjects = EstateObject.objects.filter(owner=profile)

            for item in estateObjects:

                contracts += Contract.objects.filter(estateObject=item)
                idk = item.id

                p = item.pk
                print(p)

            list_value = []

            for val in contracts:
                if selectPeriod == '3':
                    if val.dateContract.month <= 3 and val.expirationDateContract.month <= 12:
                        list_value.append(valueSerializer(val, idk))
                if selectPeriod == '6':
                    if val.dateContract.month <= 6 and val.expirationDateContract.month <= 12:
                        list_value.append(valueSerializer(val, idk))
                if selectPeriod == '9':
                    if val.dateContract.month <= 9 and val.expirationDateContract.month <= 12:
                        list_value.append(valueSerializer(val, idk))
                if selectPeriod == '12':
                    if val.dateContract.month <= 12 and val.expirationDateContract.month <= 12:
                        list_value.append(valueSerializer(val, idk))
                #else:
                #    return JsonResponse({'data': 'Ошибка. period может быть только: 3, 6, 12.'})

            return JsonResponse({'data':list_value})
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class TotalCostNowViews(APIView):
    """
    Представления для отображения общей статистики
    издержек за год
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            #try:
            propertyOwnership = EstateObject.objects.filter(owner=profile)
            totalCosts = []
            cost = []
            for item in propertyOwnership:
                totalCosts += Cost.objects.filter(estateObject=item)
                cost += ChargeUtilityBills.objects.filter(estateObject=item)
            return JsonResponse({'data':costNowSerializer_2(totalCosts,cost)})
            #except BaseException:
            #    response = JsonResponse({'data':'Ошибка серрвера'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class TotalCostOverPeriodViews(APIView):
    """
    Представления для отображения общей статистики
    издержек за выбранный период
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner() or profile.isMeneger() or profile.isTenant():
            lists_util = []
            list_total = []
            list_cahs = []
            periods = []

            utilss = []
            cashss = []
            cashss_2 = []
            cashss_3 = []
            totalss = []
            selectRealt = EstateObject.objects.filter(owner=profile)
            period = request.POST['period']



            for select in selectRealt:
                selectPeriod = Cost.objects.filter(estateObject=select)
                selectUtil = ChargeUtilityBills.objects.filter(estateObject=select)
                selectTotal = CashFlow.objects.filter(estateObject=select)


                #try:
                if period == '3':

                    for cash in selectPeriod:
                        date_cash = cash.datePayment.month
                        #print('ONE = ', list_cahs)

                    for total in selectTotal:
                        date_total = total.datePayment.month
                        #print('TWO = ', list_total)

                    for util in selectUtil:

                        date_util = util.datePayment.month
                        #print('THREE = ', lists_util)

                    #if date_util <= 3 and date_total <= 3 and date_cash <=3:
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <=3:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month
                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <=3:
                            period_2_date = period_2.datePayment.month
                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 3:
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})

                elif period == '6':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month

                        if ch <= 6:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <= 6:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 6:
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})

                elif period == '9':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <= 9:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <= 9:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 9:
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})

                elif period == '12':
                    for cash_3 in selectPeriod:
                        ch = cash_3.datePayment.month
                        if ch <= 12:
                            cashss_2.append(cost_chet(cash_3))
                            totalss.append(cost_three(cash_3))
                            cash_3_date = cash_3.datePayment.month

                    for period_2 in selectTotal:
                        pr = period_2.datePayment.month
                        if pr <= 12:
                            # totalss.append(cost_three(cash_3))
                            period_2_date = period_2.datePayment.month

                    for util_2 in selectUtil:
                        ut = util_2.datePayment.month
                        if ut <= 12:
                            utilss.append(cost_one(period_2, util_2, cash_3))
                            cashss.append(cost_two(util_2))
                            util_2_date = util_2.datePayment.month

                    return JsonResponse({'data': {
                            'total': utilss,
                            'utility_payments': cashss,
                            'operating_cost': totalss,
                            'etc': cashss_2
                    }})


        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

from django.contrib.auth.models import User
class ChangePasswordViews(APIView):
    """
    Представление для смены пароля
    """
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        #try:
        if request.user.check_password(request.POST['old_password']):
            u = User.objects.get(username__exact=request.user)
            new_pass = request.POST['new_password']
            u.set_password(new_pass)
            u.save()
            return JsonResponse({'data':'Ok'})
        else:
            response = JsonResponse({'data':'Некорректный пароль'})
            response.status_code = 403
            return response
        #except BaseException:
        #    response = JsonResponse({'data':'Ошибка серрвера'})
        #    response.status_code = 500
        #    return response

class PushMessageViews(APIView):
    """
    Представление отправки сообщений
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        #try:
        recipient = Profile.objects.get(id=request.POST['id_sender'])
        myMessage = Message()
        myMessage.newMessage(profile,recipient,request.POST['message'])
        return JsonResponse({'data':'Сообщение отправлено'})
        #except BaseException:
        #    response = JsonResponse({'data':'Ошибка серрвера'})
        #    response.status_code = 500
        #    return response

class NewMessageViews(APIView):
    """
    Представление для отображения новых сообщений
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        try:
            newMessages = Message.objects.filter(recipient=profile, status=False)
            data = []
            for newMessage in newMessages:
                data.append(
                    messageSerializer(newMessage)
                )
            return JsonResponse({'data':data})
        except BaseException:
            response = JsonResponse({'data':'Ошибка серрвера'})
            response.status_code = 500
            return response

class CountMessageViews(APIView):
    """
    Представления для отображения колличества сообщений
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        #try:
        messages = Message.objects.filter(sender=profile), Message.objects.filter(recipient=profile)
        return JsonResponse({'data':len(messages)})
        #except BaseException:
        #    response = JsonResponse({'data':'Ошибка серрвера'})
        #    response.status_code = 500
        #    return response

class RangeMessageViews(APIView):
    """
    Представления для отображения диапазона сообщений
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        #try:
        start = request.POST['start']
        finish = request.POST['finish']
        selectInterlocutor = Profile.objects.get(id=request.POST['id_recipient'])
        rangeMessages = Message.objects.filter(sender=profile,recipient=selectInterlocutor)
        #rangeMessages = Message.objects.filter(sender=selectInterlocutor,recipient=profile)
        rangem = rangeMessages #, rangeMessages_2
        data = []
        for newMessage in rangem[int(start):int(finish)]:
            data.append(
                messageSerializer(newMessage)
            )
        return JsonResponse({'data':data})
        #except BaseException:
        #    response = JsonResponse({'data':'Ошибка серрвера'})
        #    response.status_code = 500
        #    return response


class ReadMessageViews(APIView):
    """
    Представления для просмотра сообщений
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            try:
                message = Message.objects.get(id=request.POST['id_message'])
                message.markAsRead()
                return JsonResponse({'data':'Ok'})
            except BaseException:
                response = JsonResponse({'data':'Ошибка. ID сообщения не найден.'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response

class NewNatification(APIView):
    """
    Представление для отображения новых уведомлений
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isOwner():
            try:
                natifications = Natification.objects.filter(recipient=profile)
                listObjects = []
                for natification in natifications:
                    listObjects.append(natificationSerializer(natification))
                return JsonResponse({'data':listObjects})
            except BaseException:
                response = JsonResponse({'data':'Ошибка серрвера'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Нет доступа'})
            response.status_code = 403
            return response


class AllUsersViews(APIView):
    """
    Представлени для всех пользователей
    Работает только, если пользователь авторизован как
    менеджер
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isMeneger():
            listObjects = []
            clients = Profile.objects.filter(meneger = profile.id)
            print(clients)
            for client in clients:
                print(client)
                listObjects.append(profileSerializer(client))
            return JsonResponse({'data':listObjects})
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response


class DeleteUserViews(APIView):
    """
    Удаление пользователя
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isMeneger():
            try:
                client = User.objects.get(id=request.POST['id_client'])
                client.delete()
                return JsonResponse({'data':'Ok'})
            except BaseException:
                response = JsonResponse({'data':'Ошибка. id клиента не найден.'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response


class AddUserViews(APIView):
    """
    Добавление пользователя
    """
    permission_classes = [permissions.IsAuthenticated]

    def generatePassword(self):
        password = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(8))

        return password

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            #try:
            user = User()
            user.username = request.POST['username']
            user.password = self.generatePassword()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            profile = Profile()
            profile.client = user
            profile.typeUser = request.POST['type']
            profile.meneger = meneger.id
            profile.save()
            serializer = profileSerializer(profile)
            return JsonResponse(
                {"data":serializer}
            )
            #except BaseException:
            #    response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response


#Делать нужно отсюда

class AllRealtyViews(APIView):
    """
    Представлени для всей недвижемости
    Работает только, если пользователь авторизован как
    менеджер
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isMeneger():
            clients = Profile.objects.filter(meneger = profile.id)
            listRealty = []
            for client in clients:
                listRealty+=EstateObject.objects.filter(owner=client)
            listObjects = []
            for realt in listRealty:
                print(realt)
                listObjects.append(objectPropertySerializer(realt, False))
            return JsonResponse({'data':listObjects})
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class AddRealtyViews(APIView):
    """
    Добавление объекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            #try:
            realt = EstateObject()
            realt.city = request.POST['city']
            realt.address = request.POST['address']
            realt.category = request.POST['category']
            realt.area = request.POST['area']

            print(request.POST['owner'])
            user = User.objects.get(id=int(request.POST['owner']))
            realt.owner = Profile.objects.get(client=user)
            realt.description = request.POST['description']
            realt.save()
            return JsonResponse({'data':objectPropertySerializer(realt)})
            #except BaseException:
            #    response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class UpdateRealtyViews(APIView):
    """
    Редактирование объекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            #try:
            realt = EstateObject.objects.get(id=request.POST['id'])
            realt.city = request.POST['city']
            realt.address = request.POST['address']
            realt.category = request.POST['category']
            realt.area = request.POST['area']
            realt.description = request.POST['description']
            realt.img = request.POST['img']
            realt.save()
            return JsonResponse({'data':'Ok'})
            #except BaseException:
            #    response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response


class RemoveRealtyViews(APIView):
    """
    Удаление объекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            try:
                realt = EstateObject.objects.get(id=request.POST['id'])
                realt.delete()
                return JsonResponse({'data':'Ok'})
            except BaseException:
                response = JsonResponse({'data':'Ошибка. ID не найден.'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class GetImgRealtyViews(APIView):
    """
    Отправка колекции фотографий для выбранного 
    обхекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            try:
                selectRealt = EstateObject.objects.get(id=request.POST['id'])
                collections = CollectionToRealt.objects.filter(estateObject=selectRealt)
                returnObject = []
                for collection in collections:
                    returnObject.append(
                        collectionSerializer(collection)
                    )
                return JsonResponse({'data':returnObject})
            except BaseException:
                response = JsonResponse({'data':'Ошибка. ID не найден.'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class AddImgRealtyViews(APIView):
    """
    Добавление картинки из галерии для объекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            #try:
            received = request.FILES['files']
            now = datetime.now()
            nameInArr = str(received).split('.')
            expansion = '.' + nameInArr[len(nameInArr)-1]
            nameFile = str(now.date()) + '_' + str(now.time()) + expansion
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pathToFile = os.path.join(BASE_DIR, "static/dist/collections")
            pathForDB = os.path.join('/dist/collections', nameFile)
            nameFile = os.path.join(pathToFile, nameFile)
            myFile = open(nameFile, 'wb')
            for newPhoto in received:
                myFile.write(newPhoto)
            myFile.close
            collection = CollectionToRealt()
            collection.estateObject = EstateObject.objects.get(id=request.POST['id'])
            collection.fileUrl = pathForDB
            collection.save()
            return JsonResponse({'data':collectionSerializer(collection)})
            # except BaseException:
            #     response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
            #     response.status_code = 500
            #     return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class RemoveImgRealtyViews(APIView):
    """
    Удаление картинки из галерии для объекта недвижемости
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            try:
                collection = CollectionToRealt.objects.get(id=request.POST['id'])
                collection.delete()
                return JsonResponse({'data':'Ok'})
            except BaseException:
                response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class AllContractViews(APIView):
    """
    Получение всех контрактов
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        profile = Profile.objects.get(client=request.user)
        if profile.isMeneger():
            clients = Profile.objects.filter(meneger=profile.id)
            relty = EstateObject.objects.filter(owner=clients)
            real = Contract.objects.filter(estateObject=relty, status='Открыт')
            #listRealty = []
            #for client in clients:
            #    listRealty+=EstateObject.objects.filter(owner=client)
            #listContracts = []
            #for realt in listRealty:
            #    listContracts+=Contract.objects.filter(estateObject=realt, status='Открыт')
            #listObjects = []
            #for contract in listContracts:
            #    listObjects.append(contractSerializer(contract))
            return JsonResponse({'data':contractSerializer(real)})
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class AddContractViews(APIView):
    """
    Добавление контракта
    """
    permission_classes = [permissions.IsAuthenticated]

    def generateNumberContract(self):
        try:
            contract = Contract.objects.order_by('-id')[0]
            return contract.number + 1
        except BaseException:
            return 1

    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            #try:
            contract = Contract()
            contract.estateObject = EstateObject.objects.get(id=request.POST['id_realty'])
            user = User.objects.get(id=request.POST['id_rent'])
            contract.rent = Profile.objects.get(client=user)
            contract.number = self.generateNumberContract()
            contract.dateContract = datetime(
                int(request.POST['date_conclusion_year']),
                int(request.POST['date_conclusion_month']),
                int(request.POST['date_conclusion_day'])
            )
            contract.expirationDateContract = datetime(
                int(request.POST['date_end_year']),
                int(request.POST['date_end_month']),
                int(request.POST['date_end_day'])
            )
            contract.periodPaymentRent = datetime(
                int(request.POST['period_payment_rent_year']),
                int(request.POST['period_payment_rent_month']),
                int(request.POST['period_payment_rent_day'])
            )
            contract.area = request.POST['area']
            contract.price = request.POST['price']
            contract.save()
            return JsonResponse({'data':contractSerializer(contract)})
            #except BaseException:
            #    response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
            #    response.status_code = 500
            #    return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response

class CloseContractViews(APIView):
    """
    Добавление контракта
    """
    permission_classes = [permissions.IsAuthenticated]


    def post(self,request):
        meneger = Profile.objects.get(client=request.user)
        if meneger.isMeneger():
            try:
                contract = Contract.objects.get(id=request.POST['id'])
                nowDateTime = datetime.now()
                contract.expirationDateContract = datetime(
                    int(nowDateTime.year),
                    int(nowDateTime.month),
                    int(nowDateTime.day)
                )
                contract.status = 'Закрыт'
                contract.save()
                return JsonResponse({'data':'Ok'})
            except BaseException:
                response = JsonResponse({'data':'Неизвестная ошибка. Попробуйте позже'})
                response.status_code = 500
                return response
        else:
            response = JsonResponse({'data':'Неверный тип пользователя. Ожидался Менеджер'})
            response.status_code = 403
            return response