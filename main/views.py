from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from main.models import Goods, GoodsBrand, GoodsModel, PropertyBlock, Property, PropertyValue, PropertyBlockName, PropertyName, Customers, Images
from accounts.models import Branch, User
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from main.const import *
import json
import random
import string
import datetime
from django.urls import reverse_lazy
from decimal import *
# from pytils import translit
import os
from django.conf import settings
# Create your views here.


def check_status(goods):
    is_await = True if goods.filter(status=GOOD_STATUS_AWAIT) else False
    is_reject = True if goods.filter(status=GOOD_STATUS_REJECT) else False
    is_purchase = True if goods.filter(status=GOOD_STATUS_PURCHASE) else False
    is_priced = True if goods.filter(status=GOOD_STATUS_PRICED) else False
    return {'is_await': is_await, 'is_reject':is_reject, 'is_purchase':is_purchase, 'is_priced':is_priced}

def generate_id():
    good_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    try:
        is_exist = Goods.objects.get(good_id=good_id)
    except Goods.DoesNotExist:

        return good_id
    generate_id()

class GoodView(TemplateView):
    template_name = 'good_card.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):

        good_id = self.kwargs.get('good_id')
        try:
            good = Goods.objects.get(good_id=good_id)
        except Goods.DoesNotExist:
            raise Http404('Товар с ID %s не найден' % good_id)
        good_message = 'Уважаемый(ая) {0}, ваш товар {1} оценен в '.format(good.customer.name, good_id)
        context = super(GoodView, self).get_context_data(**kwargs)
        context.update({
            'good': good,
            'message': good_message
        })
        return context


class GoodsListView(ListView):

    template_name = 'goods.html'
    model = Goods
    paginate_by = 4
    page_kwarg = 'page'


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.GET:
            if self.request.user.is_staff:
                queryset = Goods.objects.all()
            else:
                queryset = Goods.objects.filter(branch__name=self.request.user.branch.name)
            brand = self.request.GET.get("brand")
            model = self.request.GET.get("model")
            status = self.request.GET.get("status")
            branch = self.request.GET.get("branch")
            if brand :
                brand = GoodsBrand.objects.filter(name__in=brand.split('--'))
                queryset = queryset.filter(brand__in=brand)
            if model:
                model = GoodsModel.objects.filter(name__in=model.split('--'))
                queryset = queryset.filter(model__in=model)
            if status:
                queryset = queryset.filter(status__in=status.split('--'))
            if branch and self.request.user.is_staff:
                branch = Branch.objects.filter(name__in=branch.split('--'))
                queryset = queryset.filter(branch__in=branch)
            return queryset
        return super(GoodsListView, self).get_queryset()
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        if self.request.user.is_staff:
            queryset = Goods.objects.all()
        else:
            queryset = Goods.objects.filter(branch__name=self.request.user.branch.name)
        page_size = self.get_paginate_by(queryset)
        queryset = queryset.order_by('-pk')
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
        return context
    

class CheckBrand(View):

    def post(self, request, *args, **kwargs):
        if request.POST:
            json_string = json.loads(request.POST['json'])
            brand_id = json_string['brandID']
            models = GoodsModel.objects.filter(brand__pk__in=brand_id)
            goods = Goods.objects.filter(brand__pk__in=brand_id)
            branchs = goods.values('branch')
            if branchs:
                branchs = Branch.objects.filter(pk__in=branchs).values('name')
            context={
                'models': list(models.values('name', 'pk'))
            }
            context.update(check_status(goods))
            context.update({'branchs': list(branchs)})
            
            return JsonResponse(context, safe=False)
        return JsonResponse('', safe=False)


class CheckStatus(View):

    def post(self, request, *args, **kwargs):
        goods = Goods.objects.all()
        if request.POST:
            json_string = json.loads(request.POST['json'])
            status = json_string['status']
            goods = goods.filter(status__in=status)
            brands = goods.values('brand')
            if brands:
                brands = GoodsBrand.objects.filter(pk__in=brands).values('name')
            branchs = goods.values('branch')
            if branchs:
                branchs = Branch.objects.filter(pk__in=branchs).values('name')
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
            json_string = json.loads(request.POST['json'])
            branch = json_string['branch']
            goods = goods.filter(branch__pk__in=branch)
            brands = goods.values('brand')
            if brands:
                brands = GoodsBrand.objects.filter(pk__in=brands).values('name')
            check_status(goods) 
            context = {'brands': list(brands)}
            context.update(check_status(goods))
            return JsonResponse(context, safe=False)
        brands = goods.values('brand')
        context= {'brands':list(brands)}
        context.update(check_status(goods))
        return JsonResponse(context, safe=False)


class BranchInfo(View):

    def post(self, request, *args, **kwargs):
        
        if request.POST:
            branch_id = request.POST.get('branch_id')
            try:
                branch = Branch.objects.get(pk=branch_id)
            except Branch.DoesNotExist:
                branch = None
            if branch:
                goods = Goods.objects.filter(branch=branch)
                balance = branch.balance
                goods_await = goods.filter(status=GOOD_STATUS_AWAIT).count()
                goods_reject = goods.filter(status=GOOD_STATUS_REJECT).count()
                goods_purchase = goods.filter(status=GOOD_STATUS_PURCHASE).count()
                goods_priced = goods.filter(status=GOOD_STATUS_PRICED).count()
                users = User.objects.filter(branch=branch).count()
                context = {
                    'balance': balance,
                    'goods_await': goods_await,
                    'goods_reject': goods_reject,
                    'goods_purchase': goods_purchase,
                    'goods_priced': goods_priced,
                    'users': users
                }
                return JsonResponse(context, safe=False)
            return HttpResponse('Branch ID not found', status=400)
        return HttpResponse('Blank query', status=400)


class GoodCreateView(View):
    template_name = 'index.html'
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})

    def post(self, request, *args, **kwargs):
        if request.POST:
            saved_images = []
            json_string = json.loads(request.POST['propertyBlocks'])
            try:
                brand_name = request.POST.get('notebook_brand').capitalize()
                model_name = request.POST.get('notebook_model').capitalize()
                customer_name = request.POST.get('seller_name').capitalize()
                customer_phone = request.POST.get('seller_phone')
            except:
                return HttpResponse('Пустая форма', status=400)
            good_description = request.POST.get('notebook_description')
            block_list = []
            for property_block in json_string['propertyBlocks']:
                prop_list = []
                block_name, block_name_created = PropertyBlockName.objects.get_or_create(name=property_block['name'])
                for properties_key in property_block['properties']:
                    property_name, property_name_created = PropertyName.objects.get_or_create(name=properties_key)
                    property_value, property_value_created = PropertyValue.objects.get_or_create(value=property_block['properties'][properties_key])
                    properti, properti_created = Property.objects.get_or_create(name=property_name, value=property_value)
                    prop_list.append(properti)
                block = PropertyBlock.objects.create(name=block_name)
                block.properties.add(*prop_list)
                block.save()
                block_list.append(block)
            good_id = generate_id()
            brand, brand_created = GoodsBrand.objects.get_or_create(name=brand_name)
            model, model_created = GoodsModel.objects.get_or_create(name=model_name, brand=brand)
            customer, customer_created = Customers.objects.get_or_create(name=customer_name, phone_number=customer_phone)
            good = Goods.objects.create(
                    good_id=good_id,
                    brand=brand, model=model,
                    user=request.user,
                    customer=customer,
                    branch=request.user.branch
                )
            if request.FILES:
                for image in request.FILES.items():
                    Images.objects.create(image=SaveImage(image[1], template_name=('{0}_{1}'.format(good.brand, good_id))).filename_root, good=good)      
            good.property_block.add(*block_list)
            good.description = good_description
            good.save()    
            return HttpResponse('success', status=200)
        return HttpResponse('Пустая форма', status=400)


class SaveImage:
    upload = None
    template_name = None
    filename = None
    filename_root = None
    filename_url = None

    def __init__(self, upload, template_name=None):
        self.upload = upload
        self.template_name = template_name
        self.response()
        
    def get_upload_path(self):
        images_folder = os.path.join(settings.MEDIA_ROOT, 'images')
        if self.template_name:
            upload_path = os.path.join(settings.MEDIA_ROOT, os.path.join(images_folder, self.template_name))
        else:
            upload_path = os.path.join(settings.MEDIA_ROOT, 'trash')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        return (self.upload.name, os.path.join(upload_path, self.upload.name), settings.MEDIA_URL + self.upload.name)

    def save(self):
        self.filename, self.filename_root, self.filename_url = self.get_upload_path()
        with open(self.filename_root, 'wb+') as out:
            for chunk in self.upload.chunks():
                out.write(chunk)
        out.close()

    def response(self):
        self.save()
        return {'filename': self.filename, 'filename_root': self.filename_root, 'filename_url': self.filename_url}

# class UploadImage(View):

#     http_method_names = ['post']
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user:
#             raise Http404('Сначала авторизутесь')
#         return super(UploadImage, self).dispatch(request, *args, **kwargs)

    

#     def post(self, request, *args, **kwargs):
        

class GoodPriced(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            message = request.POST.get('message')
            price = request.POST.get('price')
            good_id = request.POST.get('good_id')
            try:
                good = Goods.objects.get(good_id=good_id)
                branch = Branch.objects.get(name=self.request.user.branch.name)
            except Goods.DoesNotExist:
                return HttpResponse('Товар с ID {0} не найден'.format(good_id), status=400)

            good.price = price
            good.status = GOOD_STATUS_PRICED
            good.save()
            branch.balance = branch.balance - price
            branch.save()
            return HttpResponse('success', status=200)
        return HttpResponse('Пустой запрос', status=400)


class CustomerChoice(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST:
            customer_choice = request.POST.get('choice')
            good_id = request.POST.get('good_id')
            print(customer_choice, good_id)
            try:
                good = Goods.objects.get(good_id=good_id)
            except Goods.DoesNotExist:
                return HttpResponse('Товар с ID {0} не найден'.format(good_id), status=400)
            if customer_choice and customer_choice == 'purchase':
                good.status = GOOD_STATUS_PURCHASE
                good.save()
            elif customer_choice and customer_choice == 'reject':
                good.status = GOOD_STATUS_REJECT
                good.save()
            return HttpResponse('success', status=200)
        return HttpResponse('Пустой запрос', status=400)


class Notifications(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user and request.user.is_authenticated:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        goods = Goods.objects.filter(status=GOOD_STATUS_AWAIT)
        context = {
            'goods_notification': list(goods.values('brand__name', 'model__name', 'branch__name', 'good_id')),
            'count_notiification': goods.count()
        }
        return JsonResponse(context, safe=False)

class SearchByQuery(View):
    query = ''
    brand = ''
    list_types = ['brand_name', 'model_name', 'block_name', 'property_name', 'property_value']
    context = {}
    def dispatch(self, request, *args, **kwargs):
        if not request.user and request.user.is_authenticated:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST and request.POST.get('query') and request.POST.get('type_query') in self.list_types:
            self.query = request.POST.get('query')
            if request.POST.get('brand'):
                self.brand = request.POST.get('brand')
            self.search_by(request)
            return JsonResponse(self.context, safe=False)
        return JsonResponse({'result':''}, safe=False)

    def search_by(self, request):
        type_query = {
            'brand_name': self.search_by_brand_name,
            'model_name': self.search_by_model_name,
            'block_name': self.search_by_block_name,
            'property_name': self.search_by_property_name,
            'property_value': self.search_by_property_value,
        }
        return type_query[request.POST.get('type_query')]()

    def search_by_brand_name(self):
        
        brands = GoodsBrand.objects.filter(name__icontains=self.query).values('name')
        self.context.update({'result':  list(brands)[:7] if brands else ''})

    def search_by_model_name(self):
        if self.brand:
            models = GoodsModel.objects.filter(name__icontains=self.query, brand__name__icontains=self.brand).values('name')
        else:
            models = GoodsModel.objects.filter(name__icontains=self.query).values('name')
        self.context.update({'result': list(models)[:7] if models else ''})

    def search_by_block_name(self):
        block_names = PropertyBlockName.objects.filter(name__icontains=self.query).values('name')
        self.context.update({'result': list(block_names)[:7] if block_names else ''})

    def search_by_property_name(self):
        property_names = PropertyName.objects.filter(name__icontains=self.query).values('name')
        self.context.update({'result': list(property_names)[:7] if property_names else ''})
    
    def search_by_property_value(self):
        property_values = PropertyValue.objects.filter(value__icontains=self.query).values('value')
        self.context.update({'result': list(property_values)[:7] if property_values else ''})


class AddBranchBalance(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user and request.user.is_authenticated and request.user.is_staff:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST and request.POST.get('amount') and request.POST.get('branch_id'):
            try:
                branch = Branch.objects.get(pk=request.POST.get('branch_id'))
            except Branch.DoesNotExist:
                return HttpResponse('Филиал с ID {0} не найден'.format(request.POST.get('branch_id')), status=400)
            branch.balance += Decimal(request.POST.get('amount'))
            branch.save()
            return HttpResponse('Баланс успешно пополнен', status=200)
        return HttpResponse('Blank request', status=400)