from rest_framework import serializers
import base64
from django.core.files import File

from api_v1.models import *
from django.contrib.auth.models import User
import json


def nameProf(profile):
    data = {}
    user = profile.client
    data['name'] = user.first_name
    return data

def managerSer(profile):
    data = {}
    data['id'] = profile
    #data['name'] = profile.name
    return data

def profileSerializer(profile):
    """
    Серилайз профайла пользователя
    """
    data = {}
    user = profile.client
    data['id'] = user.id
    data['phone'] = user.username
    data['name'] = user.first_name
    data['surname'] = user.last_name
    data['type'] = profile.typeUser

    #data['name_meneger'] =
    #if avatar:
    #    data['avatar'] = profile.avater
    return data

def ListTenantresViewsSerializer(tenantry,profile):
    data = {}
    user = profile.client
    data['name'] = tenantry.names()
    data['description'] = tenantry.__str__()
    data['phone'] = user.username
    #data['phone'] = profileSerializer(tenantry.client.username)

    return data

def objectPropertySerializer_1(objectProperty, preview=False):
    """
    Серилайз объекта недвижимости для собственника
    """
    data = {}
    #user = profile.client
    data['id'] = objectProperty.id
    data['img'] = objectProperty.img.url
    data['city'] = objectProperty.city
    data['address'] = objectProperty.address
    data['category'] = objectProperty.category
    json.dumps(str(data['img']))
    if not preview:
        data['balance_sheet_holder'] = profileSerializer(objectProperty.owner)
        data['description'] = objectProperty.description
        data['area'] = objectProperty.area
    return data


def objectPropertySerializer(objectProperty, preview=False):
    """
    Серилайз объекта недвижимости для собственника 
    """
    data = {}
    #user = profile.client
    data['id'] = objectProperty.estateObject.id
    data['img'] = objectProperty.estateObject.img.url
    data['city'] = objectProperty.estateObject.city
    data['address'] = objectProperty.estateObject.address
    data['category'] = objectProperty.estateObject.category
    json.dumps(str(data['img']))
    if not preview:
        data['balance_sheet_holder'] = profileSerializer(objectProperty.estateObject.owner)
        data['description'] = objectProperty.estateObject.description
        data['area'] = objectProperty.estateObject.area
    return data


def indicationSerializer(meterReadings):
    """
    Серилайз показаний счётчиков
    """
    data = {}
    data['electricity'] = meterReadings.electricity
    data['hot_water'] = meterReadings.hotWater
    data['cold_water'] = meterReadings.coldWater
    data['month'] = meterReadings.dateReading.month
    data['year'] = meterReadings.dateReading.year
    return data

def utilityPaymentSerializer(utilityPayment):
    """
    Серилайз комунального платежа
    """
    data = {}
    data['name_article'] = utilityPayment.article
    data['amount_payments'] = utilityPayment.amount
    data['month'] = utilityPayment.datePayment.month
    data['year'] = utilityPayment.datePayment.year
    data['el'] = utilityPayment.elect_s
    data['pv'] = utilityPayment.hot_weat
    data['xv'] = utilityPayment.cold_weat
    data['otop'] = utilityPayment.otoplen
    data['tbo'] = utilityPayment.TBO
    data['uborka'] = utilityPayment.uborka
    return data


def objectPropertyForTenantSerializer(objectProperty,meterReadings,cashflow,utilityPayments,contract, preview=False):
    """
    Серилайз объекта недвижимости для арендатора
    """
    data = {}
    data['id'] = objectProperty.id
    data['img'] = objectProperty.img.url
    data['city'] = objectProperty.city
    data['address'] = objectProperty.address
    data['category'] = objectProperty.category

    if not preview:
        data['area'] = contract.area
        data['price'] = contract.price
        data['amount'] = cashflow.amount
        data['contract_number'] = contract.number
        data['date_contract'] = contract.dateContract
        data['expiration_date_contract'] = contract.expirationDateContract
        data['period_payment_rent'] = contract.periodPaymentRent
        data['indications'] = []
        for indication in meterReadings:
            data['indications'].append(indicationSerializer(indication))
        data['utility_payments'] = []
        for utilityPayment in utilityPayments:
            data['utility_payments'].append(
                utilityPaymentSerializer(utilityPayment)
            )
    return data

def fileSerializer(file, profile):
    """
    Серилайз файла прикреплённого к объекту недвижимости
    """
    data = {}
    user = profile.client
    data['id'] = file.id
    data['name'] = user.username
    data['url'] = file.nameFile.url
    return data

def natificationSerializer(natification):
    """
    Серилайз для уведомления
    """
    data = {}
    data['id'] = natification.id
    data['message'] = natification.message
    data['header'] = natification.header
    data['date'] = natification.date
    return data


def messageSerializer(message):
    """
    Серилайз для сообщения
    """
    data = {}
    data['message'] = message.message
    data['date'] = message.date
    data['sender'] = message.sender.id
    return data

def costNowSerializer_2(totalCosts,chargeutilitybills):
    """
    Сериализация списка издержек
    """
    returnObject = {}
    returnObject['utility_payments'] = 0
    returnObject['operating_cost'] = 0
    returnObject['etc'] = 0
    returnObject['total'] = 0

    for cost in chargeutilitybills:
        returnObject['utility_payments'] += cost.amount


    for cost in totalCosts:
        returnObject['operating_cost'] += cost.operatingCost
        returnObject['etc'] += cost.etc
        returnObject['total'] = returnObject['utility_payments'] + returnObject['operating_cost'] + returnObject['etc']
    return returnObject

def costNowSerializer(totalCosts, chargeutilitybills):
    """
    Сериализация списка издержек
    """
    returnObject = {}
    returnObject['utility_payments'] = 0
    returnObject['operating_cost'] = 0
    returnObject['etc'] = 0
    returnObject['total'] = 0

    for cost in chargeutilitybills:
        returnObject['utility_payments'] += cost.amount

    for cost in totalCosts:
        returnObject['operating_cost'] += cost.operatingCost
        returnObject['etc'] += cost.etc
        returnObject['total'] = returnObject['utility_payments'] + returnObject['operating_cost'] + returnObject['etc']
    return returnObject

def areaSerialivers(contract):
    data = {}
    #data['occupied'] = 0
    cons = 0
    for con in contract:
        cons += con.area
    data['occupied'] = cons
    return data

def areaNowSerializer(areaBusy_2,areaVacant_2,areaTotal,areaTotalS):
    """
    Сериализация списка издержек
    """
    data={}
    data['total_area'] = areaTotal
    data['occupied'] = areaTotalS[0]
    data['occupied_percent'] = areaTotalS[1]
    data['freely'] = areaTotalS[2]
    data['freely_percent'] = areaTotalS[3]
    return data

def areaOverPeriodSerializer(objectProperty, EstateObject):
    """
    Сериализация занятости площадей за период
    """
    data={}
    data['id'] = objectProperty.id
    data['area'] = EstateObject.area
    return data

def contractSerializer(contract):
    """
    Сериализация контракта
    """
    data={}
    #data['id'] = contract
    #data['estateObject'] = objectPropertySerializer(contract.estateObject)
    #data['rent'] = profileSerializer(contract.rent)
    #data['number'] = contract.number
    #data['dateContract'] = contract.dateContract
    #data['expirationDateContract'] = contract.expirationDateContract
    #data['periodPaymentRent'] = contract.periodPaymentRent
    #data['area'] = contract.area
    #data['price'] = contract.price
    #data['status'] = contract.status

    return data


def collectionSerializer(collection):
    """
    Сериаоизация коллекции
    """
    data={}
    data['id'] = collection.id
    data['fileUrl'] = collection.fileUrl.url
    return data

def periodOverSerializer(contract):
    data = {}

    #data_one = contract.dateContract.month
    #data_two = contract.expirationDateContract.month

    if contract.getBusyArea():
        data['employment'] = True
    elif contract.getVacantArea():
        data['employment'] = False
    return data

def costSerializer(cost):
    """
    Сериаоизация издержек
    """
    data={}
    data['id'] = cost.id
    data['date'] = cost.datePayment
    data['operatingCost'] = cost.operatingCost
    data['etc'] = cost.etc
    return data


def cost_one(cashflow,chargeutilitybills,Cost):
    data = {}
    mouts_cash = chargeutilitybills.datePayment.month
    if mouts_cash == 1:
        data['month'] = 'Январь'
    elif mouts_cash == 2:
        data['month'] = 'Февраль'
    elif mouts_cash == 3:
        data['month'] = 'Март'
    elif mouts_cash == 4:
        data['month'] = 'Апрель'
    elif mouts_cash == 5:
        data['month'] = 'Май'
    elif mouts_cash == 6:
        data['month'] = 'Июнь'
    elif mouts_cash == 7:
        data['month'] = 'Июль'
    elif mouts_cash == 8:
        data['month'] = 'Авгус'
    elif mouts_cash == 9:
        data['month'] = 'Сентябрь'
    elif mouts_cash == 10:
        data['month'] = 'Октябрь'
    elif mouts_cash == 11:
        data['month'] = 'Ноябрь'
    elif mouts_cash == 12:
        data['month'] = 'Декабрь'

    opercost = 0
    etccost = 0
    amout_cash = 0
    amout_cha = 0
    amout_cash += cashflow.amount
    amout_cha += chargeutilitybills.amount

    opercost += Cost.operatingCost
    etccost += Cost.etc
    data['total'] = amout_cha + opercost + etccost + amout_cash

    return data

def cost_two(chargeutilitybills):
    data = {}
    mouts_cash = chargeutilitybills.datePayment.month
    if mouts_cash == 1:
        data['month'] = 'Январь'
    elif mouts_cash == 2:
        data['month'] = 'Февраль'
    elif mouts_cash == 3:
        data['month'] = 'Март'
    elif mouts_cash == 4:
        data['month'] = 'Апрель'
    elif mouts_cash == 5:
        data['month'] = 'Май'
    elif mouts_cash == 6:
        data['month'] = 'Июнь'
    elif mouts_cash == 7:
        data['month'] = 'Июль'
    elif mouts_cash == 8:
        data['month'] = 'Авгус'
    elif mouts_cash == 9:
        data['month'] = 'Сентябрь'
    elif mouts_cash == 10:
        data['month'] = 'Октябрь'
    elif mouts_cash == 11:
        data['month'] = 'Ноябрь'
    elif mouts_cash == 12:
        data['month'] = 'Декабрь'

    ch = 0
    ch += chargeutilitybills.amount

    data['value'] = ch


    return data

def cost_three(Cost):
    data = {}
    mouts_cash = Cost.datePayment.month
    if mouts_cash == 1:
        data['month'] = 'Январь'
    elif mouts_cash == 2:
        data['month'] = 'Февраль'
    elif mouts_cash == 3:
        data['month'] = 'Март'
    elif mouts_cash == 4:
        data['month'] = 'Апрель'
    elif mouts_cash == 5:
        data['month'] = 'Май'
    elif mouts_cash == 6:
        data['month'] = 'Июнь'
    elif mouts_cash == 7:
        data['month'] = 'Июль'
    elif mouts_cash == 8:
        data['month'] = 'Авгус'
    elif mouts_cash == 9:
        data['month'] = 'Сентябрь'
    elif mouts_cash == 10:
        data['month'] = 'Октябрь'
    elif mouts_cash == 11:
        data['month'] = 'Ноябрь'
    elif mouts_cash == 12:
        data['month'] = 'Декабрь'

    data['value'] = 0

    data['value'] += Cost.operatingCost

    #data['value'] = cs

    return data


def cost_chet(Cost):
    data = {}
    mouts_cash = Cost.datePayment.month
    if mouts_cash == 1:
        data['month'] = 'Январь'
    elif mouts_cash == 2:
        data['month'] = 'Февраль'
    elif mouts_cash == 3:
        data['month'] = 'Март'
    elif mouts_cash == 4:
        data['month'] = 'Апрель'
    elif mouts_cash == 5:
        data['month'] = 'Май'
    elif mouts_cash == 6:
        data['month'] = 'Июнь'
    elif mouts_cash == 7:
        data['month'] = 'Июль'
    elif mouts_cash == 8:
        data['month'] = 'Авгус'
    elif mouts_cash == 9:
        data['month'] = 'Сентябрь'
    elif mouts_cash == 10:
        data['month'] = 'Октябрь'
    elif mouts_cash == 11:
        data['month'] = 'Ноябрь'
    elif mouts_cash == 12:
        data['month'] = 'Декабрь'

    ce = 0
    ce += Cost.etc

    data['value'] = ce

    return data



def objectcostSerializer_0(cashflow, chargeutilitybills,totalCosts):
    data = {}
    mouts_cash = totalCosts.datePayment.month
    if mouts_cash == 1:
        data['month'] = 'Январь'
    elif mouts_cash == 2:
        data['month'] = 'Февраль'
    elif mouts_cash == 3:
        data['month'] = 'Март'
    elif mouts_cash == 4:
        data['month'] = 'Апрель'
    elif mouts_cash == 5:
        data['month'] = 'Май'
    elif mouts_cash == 6:
        data['month'] = 'Июнь'
    elif mouts_cash == 7:
        data['month'] = 'Июль'
    elif mouts_cash == 8:
        data['month'] = 'Авгус'
    elif mouts_cash == 9:
        data['month'] = 'Сентябрь'
    elif mouts_cash == 10:
        data['month'] = 'Октябрь'
    elif mouts_cash == 11:
        data['month'] = 'Ноябрь'
    elif mouts_cash == 12:
        data['month'] = 'Декабрь'

    opercost = 0
    etccost = 0
    amout_cash = cashflow.amount
    amout_cha = chargeutilitybills.amount

    opercost += totalCosts.operatingCost
    etccost += totalCosts.etc
    data['total'] = amout_cash + amout_cha + opercost +etccost

    return data


def objectcostSerializer(chargeutilitybills):
    data = {}
    mouts = chargeutilitybills.datePayment.month
    if mouts == 1:
        data['month'] = 'Январь'
    elif mouts == 2:
        data['month'] = 'Февраль'
    elif mouts == 3:
        data['month'] = 'Март'
    elif mouts == 4:
        data['month'] = 'Апрель'
    elif mouts == 5:
        data['month'] = 'Май'
    elif mouts == 6:
        data['month'] = 'Июнь'
    elif mouts == 7:
        data['month'] = 'Июль'
    elif mouts == 8:
        data['month'] = 'Авгус'
    elif mouts == 9:
        data['month'] = 'Сентябрь'
    elif mouts == 10:
        data['month'] = 'Октябрь'
    elif mouts == 11:
        data['month'] = 'Ноябрь'
    elif mouts == 12:
        data['month'] = 'Декабрь'

    #for cost in chargeutilitybills:
    data['value'] = chargeutilitybills.amount

    return data

def objectcostSerializer_2(totalCosts):
    data = {}
    mouts = totalCosts.datePayment.month
    if mouts == 1:
        data['month'] = 'Январь'
    elif mouts == 2:
        data['month'] = 'Февраль'
    elif mouts == 3:
        data['month'] = 'Март'
    elif mouts == 4:
        data['month'] = 'Апрель'
    elif mouts == 5:
        data['month'] = 'Май'
    elif mouts == 6:
        data['month'] = 'Июнь'
    elif mouts == 7:
        data['month'] = 'Июль'
    elif mouts == 8:
        data['month'] = 'Авгус'
    elif mouts == 9:
        data['month'] = 'Сентябрь'
    elif mouts == 10:
        data['month'] = 'Октябрь'
    elif mouts == 11:
        data['month'] = 'Ноябрь'
    elif mouts == 12:
        data['month'] = 'Декабрь'


   #for cost in totalCosts:
    data['value'] = totalCosts.operatingCost

    return data


def objectcostSerializer_3(cashflow,totalCosts):
    data = {}
    mouts = cashflow.datePayment.month
    if mouts == 1:
        data['month'] = 'Январь'
    elif mouts == 2:
        data['month'] = 'Февраль'
    elif mouts == 3:
        data['month'] = 'Март'
    elif mouts == 4:
        data['month'] = 'Апрель'
    elif mouts == 5:
        data['month'] = 'Май'
    elif mouts == 6:
        data['month'] = 'Июнь'
    elif mouts == 7:
        data['month'] = 'Июль'
    elif mouts == 8:
        data['month'] = 'Авгус'
    elif mouts == 9:
        data['month'] = 'Сентябрь'
    elif mouts == 10:
        data['month'] = 'Октябрь'
    elif mouts == 11:
        data['month'] = 'Ноябрь'
    elif mouts == 12:
        data['month'] = 'Декабрь'


    #for cost in totalCosts:
    data['value'] = totalCosts.etc

    return data



def mouthSerializer(cashflow):
    """
    Сериаоизация даты Значения за период
    """
    data={}
    mouts = cashflow.datePayment.month
    if mouts == 1:
        data['month'] = 'Январь'
    elif mouts == 2:
        data['month'] = 'Февраль'
    elif mouts == 3:
        data['month'] = 'Март'
    elif mouts == 4:
        data['month'] = 'Апрель'
    elif mouts == 5:
        data['month'] = 'Май'
    elif mouts == 6:
        data['month'] = 'Июнь'
    elif mouts == 7:
        data['month'] = 'Июль'
    elif mouts == 8:
        data['month'] = 'Авгус'
    elif mouts == 9:
        data['month'] = 'Сентябрь'
    elif mouts == 10:
        data['month'] = 'Октябрь'
    elif mouts == 11:
        data['month'] = 'Ноябрь'
    elif mouts == 12:
        data['month'] = 'Декабрь'
    data['year'] = cashflow.datePayment.year
    data['rental_flow'] = cashflow.amount
    return data

def valueSerializer(contract,objectProperty):
    """
    Сериаоизация даты Значения за период
    """
    data={}
    data['contract_id'] = contract.id
    data['object_id'] = contract.estateObject.pk
    mouts = contract.dateContract.month
    if mouts == 1:
        data['month'] = 'Январь'
    elif mouts == 2:
        data['month'] = 'Февраль'
    elif mouts == 3:
        data['month'] = 'Март'
    elif mouts == 4:
        data['month'] = 'Апрель'
    elif mouts == 5:
        data['month'] = 'Май'
    elif mouts == 6:
        data['month'] = 'Июнь'
    elif mouts == 7:
        data['month'] = 'Июль'
    elif mouts == 8:
        data['month'] = 'Авгус'
    elif mouts == 9:
        data['month'] = 'Сентябрь'
    elif mouts == 10:
        data['month'] = 'Октябрь'
    elif mouts == 11:
        data['month'] = 'Ноябрь'
    elif mouts == 12:
        data['month'] = 'Декабрь'
    data['value'] = contract.area
    data['total_value'] = contract.estateObject.area
    return data

