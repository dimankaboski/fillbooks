# coding=utf-8
from django import template
from main.models import GoodsBrand, Branch, Goods
from main.const import *
from accounts.models import Branch
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=False)
def get_brands():
    return GoodsBrand.objects.all().values('name', 'pk')
    
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
        return u''

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
        item = [u'<li ']

        if attr:
            item.append(attr)

        if href_page:
            if href_page == 1 and urltwo:
                item.append(u'><a href="%s">' % reverse(urltwo, kwargs=dict(kwargs)))
            else:
                item.append(u'><a href="%s">' % reverse(url, kwargs=dict(kwargs, page=href_page)))
        else:
            item.append(u'><a>')

        if label:
            item.append(label)

        item.append(u'</a></li>')

        return u''.join(item)

    def display():
        last_page = 0

        if page_obj.has_previous():
            yield str_item(href_page=page_obj.previous_page_number(), label=u'←')

        for p in pages:
            if p != last_page + 1:
                yield str_item(label=u'...')

            if p == page_obj.number:
                yield str_item(attr=u'class="active"', label=p)
            else:
                yield str_item(href_page=p, label=p)

            last_page = p

        if page_obj.has_next():
            yield str_item(href_page=page_obj.next_page_number(), label=u'→')
    return mark_safe(u'<div class="pagination"><ul>%s</ul></div>' % u' '.join(display()))