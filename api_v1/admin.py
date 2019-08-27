from django.contrib import admin
from api_v1.models import *


class ProfileAdmin(admin.ModelAdmin):
     """
     Модель для расширение стандартной модели User
     """
     list_display = ('client','typeUser')

class EstateObjectAdmin(admin.ModelAdmin):
    """
    Модель объекта недвижимости
    """
    list_display = ('address',
        'city',
        'image_tag',
        'category',
        'description',
        'area',
        'owner',
)
    fields = ['img', 'image_tag','address', 'city', 'category', 'description', 'area', 'owner']
    readonly_fields = ['image_tag']

class ContractAdmin(admin.ModelAdmin):
     """
     Модель контракта
     """
     list_display = ( 'estateObject',
         'number',
         'dateContract',
         'expirationDateContract',
         'periodPaymentRent'
     )

class TenantryAdmin(admin.ModelAdmin):
     """
     Модель для хранения списков арендаторов
     """
     list_display = ('estateObject',
         'tenantry'
     )

class UploadFileAdmin(admin.ModelAdmin):
     """
     Модель для описания файлов приреплённых к объекту
     недвижимости
     """
     list_display = (
         'estateObject',
         'image_tag',
         'fileUrl',
     )
     fields = ['estateObject', 'nameFile', 'fileUrl', 'image_tag']
     readonly_fields = ['image_tag']

class CostAdmin(admin.ModelAdmin):
     """
     Модель опичывающаю издержки
     """
     list_display = ( 'estateObject',
         #'utilityPayments',
         'operatingCost',
         'etc',
         'datePayment'
     )


class MeterReadingsAdmin(admin.ModelAdmin):
     """
     Модель описывающая показания приборов учёта
     """
     list_display = ('estateObject',
         'dateReading',
         'electricity',
         'hotWater',
         'coldWater'
     )

    

class ChargeUtilityBillsAdmin(admin.ModelAdmin):
     """
     Модель описывающая начисления по коммунальным платежам
     """
     list_display = (
         'estateObject',
            'article',
            'elect_s',
            'hot_weat',
                     'cold_weat',
                     'otoplen',
                     'TBO',
                     'uborka',
            'amount',
            'datePayment'
     )

class CashFlowAdmin(admin.ModelAdmin):
     """
     Модель описывающая поступление средств за аренду
     """
     list_display = ('estateObject',
         'amount',
         'datePayment',
         'payer'
     )

class NatificationAdmin(admin.ModelAdmin):
     """
     Модель описывающая оповещения
     """
     list_display = ('header',
         'message',
         'date',
         'recipient'
     )

class MessageAdmin(admin.ModelAdmin):
     """
     Модель описывающая сообщения
     """
     list_display = ('sender',
         'message',
         'date',
         'recipient',
         'status'
     )

class CollectionToRealtAdmin(admin.ModelAdmin):
    list_display = ('estateObject', 'image_tag', 'fileUrl')
    fields = ['estateObject', 'image_tag', 'fileUrl']
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(EstateObject, EstateObjectAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Tenantry, TenantryAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(Cost, CostAdmin)
admin.site.register(MeterReadings, MeterReadingsAdmin)
admin.site.register(ChargeUtilityBills, ChargeUtilityBillsAdmin)
admin.site.register(CashFlow, CashFlowAdmin)
admin.site.register(Natification, NatificationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(CollectionToRealt, CollectionToRealtAdmin)
