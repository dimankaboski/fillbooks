# coding=utf-8
from django import template
from main.models import GoodsBrand, Branch
from main.const import GOOD_STATUS_CHOICES
from accounts.models import Branch

register = template.Library()

@register.simple_tag(takes_context=False)
def get_brands():
    return GoodsBrand.objects.all().values('name')
    
@register.simple_tag(takes_context=False)
def get_status():
    return GOOD_STATUS_CHOICES

@register.simple_tag(takes_context=False)
def get_branchs():
    return Branch.objects.all().values('name')