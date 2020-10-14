from django.db import models
from accounts.models import User
from main.const import *
from django.core.validators import RegexValidator

# Create your models here.

class GoodsBrand(models.Model):

    name = models.CharField(verbose_name="Производитель", max_length=50, unique=True)

    class Meta:
        verbose_name = ("Прозводитель")
        verbose_name_plural = ("Список производтелей")

    def __str__(self):
        return self.name


class GoodsModel(models.Model):

    name = models.CharField(verbose_name="Модель", max_length=50, unique=True)
    brand = models.ForeignKey(GoodsBrand, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Модель")
        verbose_name_plural = ("Список моделей")

    def __str__(self):
        return self.name


class PropertyValue(models.Model):

    value = models.CharField(verbose_name="Значение характеристики", max_length=50, unique=True)
    
    class Meta:
        verbose_name = ("Значение характеристики")
        verbose_name_plural = ("Список значений характеристик")

    def __str__(self):
        return self.value


class Property(models.Model):

    name = models.CharField(verbose_name="Характеристка", max_length=50, unique=True)
    value = models.ForeignKey(PropertyValue, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Характеристика")
        verbose_name_plural = ("Список характеристик")

    def __str__(self):
        return self.name



class PropertyBlock(models.Model):

    name = models.CharField(verbose_name="Блок характеристик", max_length=50, unique=True)
    properties = models.ManyToManyField(Property, verbose_name="Характеристики")
    class Meta:
        verbose_name = ("Блок характеристик")
        verbose_name_plural = ("Список блоков характеристик")

    def __str__(self):
        return self.name


class Customers(models.Model):

    name = models.CharField(verbose_name="Имя клиента", max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть указан в формате +71234567890")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    
    
    class Meta:
        verbose_name = ("Клиент")
        verbose_name_plural = ("Список клиентов")

    def __str__(self):
        return self.phone_number


class Goods(models.Model):
    good_id = models.CharField(verbose_name="ID товара", max_length=16, unique=True)
    brand = models.ForeignKey(GoodsBrand, verbose_name="Производитель", on_delete=models.CASCADE)
    model = models.ForeignKey(GoodsModel, verbose_name="Модель", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Добавивший пользователь", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, verbose_name="Клиент", on_delete=models.CASCADE)
    branch = models.CharField(verbose_name="Филиал", max_length=50)
    price = models.CharField(verbose_name="Цена", max_length=10, blank=True, default='')
    status = models.CharField(verbose_name="Статус", max_length=20, choices=GOOD_STATUS_CHOICES, default=GOOD_STATUS_AWAIT)
    property_block = models.ManyToManyField(PropertyBlock, verbose_name="Блоки характеристик")
    description = models.TextField(verbose_name="Описание", blank=True, default='')

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Список товаров")

    def __str__(self):
        return self.good_id