from django.shortcuts import render
from django.views.generic import ListView, View
from main.models import Goods, GoodsBrand, GoodsModel
from django.http import HttpResponse, JsonResponse
from main.const import *


# Create your views here.
def index(request):
    return render(request, 'index.html', context={})

def goods(request):
    return render(request, 'goods.html', context={})

def check_status(goods):
    is_await = True if goods.filter(status=GOOD_STATUS_AWAIT) else False
    is_reject = True if goods.filter(status=GOOD_STATUS_REJECT) else False
    is_purchase = True if goods.filter(status=GOOD_STATUS_PURCHASE) else False
    is_priced = True if goods.filter(status=GOOD_STATUS_PRICED) else False
    return {'is_await': is_await, 'is_reject':is_reject, 'is_purchase':is_purchase, 'is_priced':is_priced}


class GoodsListView(ListView):

    template_name = 'goods.html'
    model = Goods
    
    def get_queryset(self):
        if self.request.GET:
            queryset = Goods.objects.all()

            brand = self.request.GET.get("brand")
            model = self.request.GET.get("model")
            status = self.request.GET.get("status")
            branch = self.request.GET.get("branch")
            if brand:
                brand = GoodsBrand.objects.filter(name__in=brand.split('-'))
                queryset = queryset.filter(brand__in=brand)
            if model:
                model = GoodsModel.objects.filter(name__in=model.split('-'))
                queryset = queryset.filter(model__in=model)
            if status:
                queryset = queryset.filter(status__in=status.split('-'))
            if branch:
                queryset = queryset.filter(branch__in=status.split('-'))
            return queryset
        return super(GoodsListView, self).get_queryset()
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'goods': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'goods': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super().get_context_data(**context)
    

class CheckBrand(View):
    def post(self, request, *args, **kwargs):
        if request.POST:
            brand_id = request.POST.get('brandID')
            models = GoodsModel.objects.filter(brand__pk__in=brand_id)
            goods = Goods.objects.filter(brand__pk__in=brand_id)
            branchs = goods.values('branch')
            context={'models': list(models)}
            context.update(check_status(goods))
            context.update({'branchs': branchs})
            return JsonResponse(context, safe=False)
        return JsonResponse('', safe=False)


class CheckStatus(View):
    def post(self, request, *args, **kwargs):
        goods = Goods.objects.all()
        if request.POST:
            status = request.POST.get('status')
            goods = goods.filter(status__in=status).values('brand')
            brands = goods.values('brand')
            branchs = goods.values('branch')
            context = {'brands': list(brands), 'branchs': list(branchs)}
            return JsonResponse(context, safe=False)
        brands = goods.values('brand')
        branchs = goods.values('branch')
        context = {'brands': list(brands), 'branchs': list(branchs)}
        return JsonResponse(context, safe=False)


class CheckBranch(View):
    def post(self, request, *args, **kwargs):
        goods = Goods.objects.all()
        if request.POST:
            branch = request.POST.get('branch')
            goods = goods.filter(branch__pk__in=branch)
            brands = goods.values('brand')
            check_status(goods) 
            context = {'brands': list(brands)}
            context.update(check_status(goods))
            return JsonResponse(context, safe=False)
        brands = goods.values('brand')
        context= {'brands':list(brands)}
        context.update(check_status(goods))
        return JsonResponse(context, safe=False)

def login(request):
    return render(request, 'login.html', context={})

def good_card(request):
    return render(request, 'good_card.html', context={})

def register(request):
    return render(request, 'register.html', context={})