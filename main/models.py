from django.db import models
from accounts.models import User, Branch
from main.const import *
from django.core.validators import RegexValidator
from django.conf import settings

# Create your models here.

class GoodsBrand(models.Model):

    name = models.CharField(verbose_name="Производитель", max_length=50, unique=True)

    class Meta:
        verbose_name = ("Прозводитель")
        verbose_name_plural = ("Список производтелей")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(GoodsBrand, self).save(*args, **kwargs)


class GoodsModel(models.Model):

    name = models.CharField(verbose_name="Модель", max_length=50, unique=True)
    brand = models.ForeignKey(GoodsBrand, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Модель")
        verbose_name_plural = ("Список моделей")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(GoodsModel, self).save(*args, **kwargs)


class PropertyValue(models.Model):

    value = models.CharField(verbose_name="Значение характеристики", max_length=50, unique=True)
    
    class Meta:
        verbose_name = ("Значение характеристики")
        verbose_name_plural = ("Список значений характеристик")

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        self.value = self.value.capitalize()
        return super(PropertyValue, self).save(*args, **kwargs)

class PropertyName(models.Model):
    name = models.CharField(verbose_name="Характеристка", max_length=50, unique=True)
    class Meta:
        verbose_name = ("Название характеристик")
        verbose_name_plural = ("Список названий характеристик")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(PropertyName, self).save(*args, **kwargs)


class Property(models.Model):

    name = models.ForeignKey(PropertyName, on_delete=models.CASCADE)
    value = models.ForeignKey(PropertyValue, on_delete = models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Характеристика")
        verbose_name_plural = ("Список характеристик")

    def __str__(self):
        return self.name.name


class PropertyBlockName(models.Model):
    name = models.CharField(verbose_name="Блок характеристик", max_length=50, unique=True)
    class Meta:
        verbose_name = ("Название блока характеристик")
        verbose_name_plural = ("Список названий блоков характеристик")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(PropertyBlockName, self).save(*args, **kwargs)

class PropertyBlock(models.Model):

    name = models.ForeignKey(PropertyBlockName, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, verbose_name="Характеристики")
    class Meta:
        verbose_name = ("Блок характеристик")
        verbose_name_plural = ("Список блоков характеристик")

    def __str__(self):
        return self.name.name


class Customers(models.Model):

    name = models.CharField(verbose_name="Имя клиента", max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть указан в формате +71234567890")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    
    
    class Meta:
        verbose_name = ("Клиент")
        verbose_name_plural = ("Список клиентов")

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(Customers, self).save(*args, **kwargs)


class Goods(models.Model):
    good_id = models.CharField(verbose_name="ID товара", max_length=6, unique=True)
    brand = models.ForeignKey(GoodsBrand, verbose_name="Производитель", on_delete=models.CASCADE)
    model = models.ForeignKey(GoodsModel, verbose_name="Модель", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Добавивший пользователь", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, verbose_name="Клиент", on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, verbose_name="Филиал", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Цена",max_digits=8, decimal_places=2, blank=True)
    status = models.CharField(verbose_name="Статус", max_length=20, choices=GOOD_STATUS_CHOICES, default=GOOD_STATUS_AWAIT)
    property_block = models.ManyToManyField(PropertyBlock, verbose_name="Блоки характеристик")
    description = models.TextField(verbose_name="Описание", blank=True, default='')


    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Список товаров")

    def __str__(self):
        return self.good_id

    def get_one_image(self):
        try:
            return self.images.all()[0]
        except:
            return None

class Images(models.Model):
    image = models.ImageField()
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images')

    def get_filename_url(self):
        url = self.image.name.split('media/')
        filename_url = settings.MEDIA_URL + url[1]
        return filename_url
