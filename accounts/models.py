from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
class Position(models.Model):

    name = models.CharField(verbose_name="Должность", max_length=50)

    class Meta:
        verbose_name = ("Должность")
        verbose_name_plural = ("Список должностей")

    def __str__(self):
        return self.name


class Branch(models.Model):

    name = models.CharField(verbose_name="Филиал", max_length=50)
    address = models.CharField(verbose_name="Адрес филиала", max_length=200, blank=True, default='')
    balance = models.DecimalField(verbose_name="Баланс филиала",max_digits=12, decimal_places=2)
    # balance = models.CharField(verbose_name="Баланс филиала", max_length=50)

    class Meta:
        verbose_name = ("Филиал")
        verbose_name_plural = ("Список филиалов")

    def __str__(self):
        return self.name




class User(AbstractUser):
    middle_name = models.CharField(verbose_name="Отчество", max_length=50, blank=True, default='')
    position = models.ForeignKey(Position, on_delete = models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, blank=True, null=True)
    is_admin = models.BooleanField(verbose_name="Админ", default=False)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return self.username
    