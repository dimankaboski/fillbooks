from django.contrib import admin
from main.models import *
# Register your models here.


class GoodsBrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class GoodsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    search_fields = ['name', 'brand']


class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ['value']
    search_fields = ['value']


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    search_fields = ['name', 'value']


class PropertyBlockAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CustomersAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number']
    search_fields = ['phone_number']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['good_id', 'brand', 'model', 'branch', 'status']
    search_fields = ['good_id', 'brand', 'model', 'branch', 'status']


admin.site.register(GoodsBrand, GoodsBrandAdmin)
admin.site.register(GoodsModel, GoodsModelAdmin)
admin.site.register(PropertyValue, PropertyValueAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyBlock, PropertyBlockAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Goods, GoodsAdmin)