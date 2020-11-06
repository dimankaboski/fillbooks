# coding=utf-8
from django import template
from main.models import GoodsBrand, Branch, Goods
from main.const import *
from accounts.models import Branch
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=False)
def get_brands(request):
    if request.user.is_staff:
        return Goods.objects.all().values('brand__name', 'brand__pk').distinct()
    return Goods.objects.filter(branch__name=request.user.branch.name).values('brand__name', 'brand__pk').distinct()
    
@register.simple_tag(takes_context=False)
def get_status():
    statuses = [GOOD_STATUS_AWAIT, GOOD_STATUS_REJECT, GOOD_STATUS_PURCHASE, GOOD_STATUS_PRICED]
    return statuses

@register.simple_tag(takes_context=False)
def get_branchs():
    return Branch.objects.all().values('name', 'pk')

@register.simple_tag(takes_context=False)
def get_images(good_id):
    try:
        good = Goods.objects.get(good_id=good_id)
    except Goods.DoesNotExist:
        return None
    return good.images.all()

# @register.simple_tag(takes_context=False)
# def get_one_image(good_id):
#     try:
#         good = Goods.objects.get(good_id=good_id)
#     except Goods.DoesNotExist:
#         return None
#     return good.images()[0]


@register.simple_tag
def render_pagination(page_obj, url, urltwo=None, **kwargs):
    """
    Паджинация, формирует меню выбора страниц
    @param page_obj:
    @param url: наименование URL (абсолютный)
    @param kwargs: список параметров для URL
    @return: safe str
    """
    pages_count = page_obj.paginator.num_pages
    # page = page_obj.number

    if pages_count <= 1:
        return ''

    if pages_count <= 10:
        pages = page_obj.paginator.page_range
    else:
        pages = sorted(
            set(
                range(1, 4)
            ) | set(
                range(max(1, page_obj.number - 2), min(page_obj.number + 3, pages_count + 1))
            ) | set(
                range(pages_count - 2, pages_count + 1)
            )
        )

    def str_item(href_page=None, label=None, attr=None):
        item = ['<li ']

        if attr:
            item.append(attr)

        if href_page:
            if href_page == 1 and urltwo:
                item.append('><a href="%s">' % reverse(urltwo, kwargs=dict(kwargs)))
            else:
                item.append('><a href="%s">' % reverse(url, kwargs=dict(kwargs, page=href_page)))
        else:
            item.append('><a>')

        if label:
            item.append(label)

        item.append('</a></li>')

        return ''.join(item)

    def display():
        last_page = 0


        for p in pages:
            if p != last_page + 1:
                yield str_item(label='...')

            if p == page_obj.number:
                yield str_item(attr='class="active"', label=str(p))
            else:
                yield str_item(href_page=p, label=str(p))

            last_page = p


    return mark_safe('<div class="pagination"><ul>%s</ul></div>' % ' '.join(display()))