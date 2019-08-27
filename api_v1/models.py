from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.safestring import mark_safe
from rest_framework.utils import json


class Profile(models.Model):
    """
    Модель для расширение стандартной модели User
    """
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    typeUser = models.TextField("Тип пользователя", max_length=200)
    meneger = models.IntegerField(blank=True,default=0, verbose_name="ID Менеджера")

    def __str__(self):
        return self.typeUser + " " + self.client.first_name

    def isTenant(self):
        """
        Проверяет является ли пользователь арендатором
        """
        if self.typeUser == 'Арендатор':
            return True
        else:
            return False

    def isOwner(self):
        """
        Проверяет является ли пользователь собственником
        """
        if self.typeUser == 'Собственник':
            return True
        else:
            return False

    def isMeneger(self):
        """
        Проверяет является ли пользователь менеджером
        """
        if self.typeUser == 'Менеджер':
            return True
        else:
            return False



    def getTotalArea(self):
        """
        Возвращает общую площадь для данного полльзователя
        """
        area = 0
        for item in EstateObject.objects.filter(owner=self):
            area += item.area
        return area

    def getTotalAreaSs(self):
        """
        Возвращает общую площадь для данного полльзователя
        """
        area = 0
        occupied = 0
        for item in EstateObject.objects.filter(owner=self):
            area += item.area

        for oc in Contract.objects.filter(rent=self):
            occupied += oc.area
        Procent = occupied / self.getTotalArea()
        Procent *= 100

        freely = area-occupied

        proc_free = 100-Procent
        return occupied, round(Procent,1), freely, round(proc_free, 1)

    def getBusyArea_2(self):
        """
        22222
        """
        #statusRent = True
        area = 0
        for item in EstateObject.objects.filter(owner=self):
            area += item.area
        areaOfProcent = area/self.getTotalArea()
        areaOfProcent *= 100
        return (area,areaOfProcent)

    def getVacantArea_2(self):
        """
        2222
        """
        #statusRent = False
        area = 0
        for item in EstateObject.objects.filter(owner=self):
            area += item.area

        areaOfProcent = area/self.getTotalArea()
        areaOfProcent *= 100
        #print(area)
        #print(area/self.getTotalArea())
        #print(areaOfProcent)
        return (area,areaOfProcent)



    def getBusyArea(self):
        """
        Возвращает занятую площадь для данного полльзователя
        """
        statusRent = True
        area = 0
        for item in EstateObject.objects.filter(owner=self, statusRent=True):
            area += item.area
        #areaOfProcent = area/self.getTotalArea()
        #areaOfProcent *= 100

        return statusRent

    def getVacantArea(self):
        """
        Возвращает свободную площадь дляданного полльзователя
        """
        statusRent = False
        area = 0
        for item in EstateObject.objects.filter(owner=self, statusRent=False):
            area += item.area
        #areaOfProcent = area/self.getTotalArea()
        #areaOfProcent *= 100
        return statusRent

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class EstateObject(models.Model):
    """
    Модель объекта недвижимости
    """
    img = models.ImageField(verbose_name='Изображение', upload_to=u'images/%Y/%m/%d/', blank=True, null=True)
    city = models.TextField('Название города', max_length=100)
    address = models.TextField('Адрес объекта', max_length=100)
    category = models.TextField('Категория объекта', max_length=100)
    description = models.TextField('Описание объекта', max_length=300)
    area = models.IntegerField('Площадь объекта')
    owner = models.ForeignKey(Profile, models.SET_NULL,blank=True, null=True,
                              verbose_name="Балансодержатель", related_name='owner_set')


    def getBusyArea(self):
        """
        Возвращает занятую площадь для данного объекта
        """
        area = EstateObject.area
        statusRent = True
        return statusRent, area

    def getVacantArea(self):
        """
        Возвращает свободную площадь дляданного объекта
        """
        area = EstateObject.area
        statusRent = False

        return statusRent,area


    def __str__(self):
        return self.city + " " + self.address

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" style="width: 85px; height:85px;" />' % self.img.url)
        else:
            return 'Изображеие не найдена'

    image_tag.short_description = 'Изображение'

class Contract(models.Model):
    """
    Модель контракта
    """
    estateObject = models.ForeignKey(EstateObject, models.SET_NULL,blank=True, null=True,
                                     verbose_name="Объект недвижимости")
    rent = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True,
                             verbose_name="Арендующий", related_name='rent_set_contract')
    number = models.BigIntegerField('Номер кантракта')
    dateContract = models.DateField(verbose_name='Дата заключения контракта')
    expirationDateContract = models.DateField(verbose_name='Дата окончания контракта') 
    periodPaymentRent = models.DateField(verbose_name='Срок оплаты аренды')
    area = models.IntegerField('Площадь объекта')
    price = models.FloatField('Цена за квадрат')
    status = models.TextField(default='Открыт')




    def __str__(self):
        return str(self.rent)

    def Prices(self):
        return self.price


    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"

class Tenantry(models.Model):
    """
    Модель для хранения списков арендаторов
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    tenantry = models.ForeignKey(Profile, on_delete=models.CASCADE, 
        verbose_name="Арендатор")
    def __str__(self):
        returnStr = self.estateObject.city + " " + self.estateObject.address
        returnStr += " - " + self.tenantry.client.last_name 
        returnStr += " " + self.tenantry.client.first_name
        return returnStr
    def names(self):
        returnname = self.tenantry.client.first_name
        return returnname
    class Meta:
        verbose_name = "Арендатор"
        verbose_name_plural = "Арендаторы"

class UploadFile(models.Model):
    """
    Модель для описания файлов приреплённых к объекту
    недвижимости
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    nameFile = models.FileField(verbose_name="Файл")
    fileUrl = models.TextField('Путь к файлу', max_length=400)
    def __str__(self):
        return self.nameFile.url
    class Meta:
        verbose_name = "Загруженый файл"
        verbose_name_plural = "Загруженные файлы"

    def image_tag(self):
        if self.nameFile:
            return mark_safe('<img src="%s" style="width: 85px; height:85px;" />' % self.nameFile.url)
        else:
            return 'Файл не найден'

    image_tag.short_description = 'Файл'

class CollectionToRealt(models.Model):
    """
    Модель для описания коллекции фотографий для объекта недвижемости
    """
    estateObject = models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    fileUrl = models.ImageField('Путь к файлу', max_length=400)
    def __str__(self):
        return self.fileUrl.url
    class Meta:
        verbose_name = "Коллекция фотографий"
        verbose_name_plural = "Коллекции фотографий"

    def image_tag(self):
        if self.fileUrl:
            return mark_safe('<img src="%s" style="width: 85px; height:85px;" />' % self.fileUrl.url)
        else:
            return 'Файл не найден'

    image_tag.short_description = 'Файл'

class Cost(models.Model):
    """
    Модель опиcывающаю издержки
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    operatingCost = models.FloatField('Эксплуатационный затраты', default=0)
    etc = models.FloatField('Прочее', default=0)
    datePayment = models.DateField(verbose_name='Дата платежа')
    def __str__(self):
        return self.estateObject.city + " " + self.estateObject.address
    class Meta:
        verbose_name = "Издержка"
        verbose_name_plural = "Издержки"

    def getTotal(self):
        gettot = self.operatingCost + self.etc
        return gettot
    
    @staticmethod
    def getFirstRecord(selectRealt):
        costs = Cost.objects.filter(estateObject=selectRealt).order_by('datePayment')
        return costs[0]
    

class MeterReadings(models.Model):
    """
    Модель описывающая показания приборов учёта
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    dateReading = models.DateField(verbose_name="Дата снятия показаний")
    electricity = models.FloatField('Электроэненргия')
    hotWater = models.FloatField('Горячая вода')
    coldWater = models.FloatField('Холодная вода')
    def __str__(self):
        return self.estateObject.city + " " + self.estateObject.address
    class Meta:
        verbose_name = "Показание приборов"
        verbose_name_plural = "Показания приборов"

class ChargeUtilityBills(models.Model):
    """
    Модель описывающая начисления по коммунальным платежам
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    article = models.TextField('Статья начисления')
    elect_s = models.FloatField('Электроснабжение')
    hot_weat = models.FloatField('Подогрев воды')
    cold_weat = models.FloatField('Холодное водоснобжение')
    otoplen = models.FloatField('Отопление')
    TBO = models.FloatField('Вызов ТБО')
    uborka = models.FloatField('Уборка с места общего пользования')
    amount = models.FloatField('Сумма платежа')
    datePayment = models.DateField(verbose_name="Дата платежа")
    def __str__(self):
        return self.estateObject.city + " " + self.estateObject.address
    class Meta:
        verbose_name = "Комунальный платеж"
        verbose_name_plural = "Комунальные платежи"

class CashFlow(models.Model):
    """
    Модель описывающая поступление средств за аренду
    """
    estateObject =  models.ForeignKey(EstateObject, on_delete=models.CASCADE, 
        verbose_name="Объект недвижимости")
    amount = models.FloatField('Сумма платежа')
    datePayment = models.DateField(verbose_name="Дата платежа")
    payer =  models.ForeignKey(Profile, on_delete=models.CASCADE, 
        verbose_name="Плательщик")
    def __str__(self):
        return self.estateObject.city + " " + self.estateObject.address
    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Денежные поступления"


class Natification(models.Model):
    """
    Модель описывающая уведомление
    """
    header = models.TextField(verbose_name="Заголовок", max_length=300)
    message = models.TextField(verbose_name="Текст сообщения", max_length=500)
    date = models.DateField(verbose_name="Дата отправления")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, 
        verbose_name="Получатель")
    def __str__(self):
        return self.header + " - " + self.recipient.client.last_name + " " + self.recipient.client.first_name
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

class Message(models.Model):
    """
    Модель описывающая сообщение
    """
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE,
        verbose_name="Отпровитель", related_name='sender_set')
    message = models.TextField(verbose_name="Текст сообщения", max_length=1000)
    date = models.DateField(verbose_name="Дата отправления") 
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, 
        verbose_name="Получатель", related_name='recipient_set')
    status = models.BooleanField(default=False, verbose_name="Статус просмотра")
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщение"

    def __str__(self):
        returnStr =  "  от  " + str(self.sender.client) + "  сообщение  " + self.message
        returnStr += "  для  " + str(self.recipient.client)
        return returnStr

    def newMessage(self,sender,recipient,message):
        """
        Добавление нового сообщения
        """
        self.sender = sender
        self.message = message
        self.date = datetime.datetime.now()
        self.recipient = recipient
        self.save()

    def markAsRead(self):
        """
        Помечает сообщение как прочитанное
        """
        self.status = True

