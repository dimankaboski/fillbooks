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
from pytils import translit
import os
from django.conf import settings





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
    paginate_by = 10
    page_kwarg = 'page'
    context_object_name = 'goods'
    ordering = '-pk'

    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Goods.objects.all().exclude(status=GOOD_STATUS_SHIPPED)
        else:
            queryset = Goods.objects.filter(branch__name=self.request.user.branch.name).exclude(status=GOOD_STATUS_SHIPPED)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        if self.request.GET:
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
        return queryset
    

class GoodsShippListView(GoodsListView):
    template_name = 'goods_shipping'

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Goods.objects.filter(status=GOOD_STATUS_SHIPPED)
        else:
            queryset = Goods.objects.filter(branch__name=self.request.user.branch.name, status=GOOD_STATUS_SHIPPED)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

class CheckBrand(View):
    type_filter = 'brandID'
    queryset = Goods.objects.all()

    def get_queryset(self, data):
        queryset = self.queryset.filter(brand__pk__in=data)
        return queryset

    def get_context_data(self, json):
        data = self.get_data(json)
        queryset = self.get_queryset(data)
        models = queryset.values('model__name', 'model__pk').distinct()
        branchs = queryset.values('branch__name').distinct()
        context = {
            'models': list(models),
            'branchs': list(branchs)            
        }
        context.update(self.check_status(queryset))
        return context

    def check_status(self, queryset):
        is_await = True if queryset.filter(status=GOOD_STATUS_AWAIT) else False
        is_reject = True if queryset.filter(status=GOOD_STATUS_REJECT) else False
        is_purchase = True if queryset.filter(status=GOOD_STATUS_PURCHASE) else False
        is_priced = True if queryset.filter(status=GOOD_STATUS_PRICED) else False
        return {'is_await': is_await, 'is_reject':is_reject, 'is_purchase':is_purchase, 'is_priced':is_priced}

    def get_data(self, json):
        type_filter = self.get_type_filter()
        data = json[type_filter]
        return data
    
    def get_type_filter(self):
        return self.type_filter
        
    def post(self, request, *args, **kwargs):
        if request.POST:
            json_string = json.loads(request.POST['json'])
            context = self.get_context_data(json_string)         
            return JsonResponse(context, safe=False)
        return JsonResponse('', safe=False)


class CheckStatus(CheckBrand):
    type_filter = 'status'
    
    def get_queryset(self, data=None):
        if data:
            self.queryset = self.queryset.filter(status__in=data)
        return self.queryset

    def get_context_data(self, json=None):
        if json:
            data = self.get_data(json)
            queryset = self.get_queryset(data)
        else:
            queryset = self.get_queryset()
        
        brands = queryset.values('brand__name', 'brand__pk').distinct()
        branchs = queryset.values('branch__name').distinct()
        context = {
            'brands': list(brands),
            'branchs': list(branchs)                        
        }
        return context

    def post(self, request, *args, **kwargs):
        if not request.POST:
            context = self.get_context_data()
            return JsonResponse(context, safe=False)
        return super().post(request, *args, **kwargs)

class CheckBranch(CheckStatus):

    type_filter = 'branch'

    def get_queryset(self, data=None):
        if data:
            self.queryset = self.queryset.filter(branch__pk__in=data)
        return self.queryset

    def get_context_data(self, json):
        if json:
            data = self.get_data(json)
            queryset = self.get_queryset(data)
        else:
            queryset = self.get_queryset()

        brands = queryset.values('brand__name', 'brand__pk').distinct()
        context = {
            'brands': list(brands),           
        }
        context.update(self.check_status(queryset))
        return context


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
                if property_block['name']:
                    block_name, block_name_created = PropertyBlockName.objects.get_or_create(name=property_block['name'].capitalize())
                    for properties_key in property_block['properties']:
                        if properties_key and isinstance(properties_key, str):
                            property_name, property_name_created = PropertyName.objects.get_or_create(name=properties_key.capitalize())
                            if property_block['properties'][properties_key] and isinstance(property_block['properties'][properties_key], str):
                                property_value, property_value_created = PropertyValue.objects.get_or_create(value=property_block['properties'][properties_key].capitalize())
                                properti, properti_created = Property.objects.get_or_create(name=property_name, value=property_value)
                                prop_list.append(properti)
                    block = PropertyBlock.objects.create(name=block_name)
                    if prop_list:
                        block.properties.add(*prop_list)
                    block.save()
                    if block:
                        block_list.append(block)
            good_id = generate_id()
            if brand_name:
                brand, brand_created = GoodsBrand.objects.get_or_create(name=brand_name)
            if model_name:
                model, model_created = GoodsModel.objects.get_or_create(name=model_name, brand=brand)
            customer, customer_created = Customers.objects.get_or_create(phone_number=customer_phone)
            customer.name = customer_name
            customer.save()
            good = Goods.objects.create(
                    good_id=good_id,
                    brand=brand, model=model,
                    user=request.user,
                    customer=customer,
                    branch=request.user.branch
                )
            if request.FILES:
                for image in request.FILES.items():
                    image = SaveImage(image[1], folder_name=('{0}_{1}'.format(translit.slugify(good.brand), good_id)))
                    image_info = image.image_info()
                    if image_info['is_saved']:
                        Images.objects.create(image=image_info['filename_root'], good=good)      
            good.property_block.add(*block_list)
            good.description = good_description
            good.save()    
            return HttpResponse('success', status=200)
        return HttpResponse('Пустая форма', status=400)


class SaveImage:
    upload = None
    folder_name = None

    def __init__(self, upload, folder_name=None):
        self.upload = upload
        self.folder_name = folder_name
    
    def get_folder_name(self):
        return self.folder_name

    def get_upload_path(self):
        images_folder = os.path.join(settings.MEDIA_ROOT, 'images')
        image_name = self.upload.name
        folder_name = self.get_folder_name()
        if folder_name:
            upload_path = os.path.join(settings.MEDIA_ROOT, os.path.join(images_folder, folder_name))
        else:
            upload_path = os.path.join(settings.MEDIA_ROOT, 'trash')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        return (image_name, os.path.join(upload_path, image_name), settings.MEDIA_URL + image_name)

    def save(self, filename_root):        
        with open(filename_root, 'wb+') as out:
            for chunk in self.upload.chunks():
                out.write(chunk)
        out.close()

    def is_saved(self, filename_root):
        return os.path.isfile(filename_root)

    def image_info(self):
        filename, filename_root, filename_url = self.get_upload_path()
        is_saved = False
        if filename_root:
            self.save(filename_root)
            is_saved = self.is_saved(filename_root)
        context = {
            'is_saved': is_saved,
            'filename': filename,
            'filename_root': filename_root,
            'filename_url': filename_url
        }
        return context


class GoodPriced(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            message = request.POST.get('message')
            good_id = request.POST.get('good_id')
            price = request.POST.get('price')
            try:
                good = Goods.objects.get(good_id=good_id)
            except Goods.DoesNotExist:
                return HttpResponse('Товар с ID {0} не найден'.format(good_id), status=400)
            good.price = price
            good.status = GOOD_STATUS_PRICED
            good.save()
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
            try:
                good = Goods.objects.get(good_id=good_id)
                branch = Branch.objects.get(name=self.request.user.branch.name)
            except Goods.DoesNotExist:
                return HttpResponse('Товар с ID {0} не найден'.format(good_id), status=400)
            if customer_choice and customer_choice == 'purchase':
                good.status = GOOD_STATUS_PURCHASE
                good.save()
                if branch and good:
                    if (branch.balance - good.price) >= 0:
                        branch.balance = Decimal(branch.balance) - Decimal(good.price)
                        branch.save()
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
        goods = Goods.objects.filter(status=GOOD_STATUS_AWAIT).order_by('-pk')
        context = {
            'goods_notification': list(goods.values('brand__name', 'model__name', 'branch__name', 'good_id')),
            'count_notiification': goods.count()
        }
        return JsonResponse(context, safe=False)


class SearchByQuery(View):
    list_types = ['brand_name', 'model_name', 'block_name', 'property_name', 'property_value']
    obj_count = 7
    brand = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user and request.user.is_authenticated:
            raise Http404('Сначала авторизуйтесь')
        return super().dispatch(request, *args, **kwargs)

    def get_self_brand(self):
        return self.brand
        
    def get_list_types(self):
        return self.list_types
    
    def get_obj_count(self):
        return self.obj_count

    def get_context_data(self, obj_list=None):
        context = {
            'result': ''
        }
        if obj_list:
            obj_count = self.get_obj_count()
            if obj_count and isinstance(obj_count, int):
                context['result'] = list(obj_list)[:obj_count]
                return context
            context['result'] = list(obj_list)
            return context
        return context      
        
    
    def post(self, request, *args, **kwargs):
        response = self.get_context_data()
        if request.POST:
            query = request.POST.get('query')
            type_query = request.POST.get('type_query')
            list_types = self.get_list_types()
            self.brand = request.POST.get('brand')
            if query and type_query in list_types:
                response = self.search_by(request, query, type_query)
                return JsonResponse(response, safe=False)
        return JsonResponse(response, safe=False)

    def search_by(self, request, query, type_query, brand=None):
        type_query_choice = {
            'brand_name': self.search_by_brand_name,
            'model_name': self.search_by_model_name,
            'block_name': self.search_by_block_name,
            'property_name': self.search_by_property_name,
            'property_value': self.search_by_property_value,
        }
        search_result = type_query_choice[type_query](query)
        return search_result

    def search_by_brand_name(self, query):        
        brands = GoodsBrand.objects.filter(name__icontains=query).values('name')
        context = self.get_context_data(brands)
        return context

    def search_by_model_name(self, query):
        brand = self.get_self_brand()
        if brand:
            models = GoodsModel.objects.filter(name__icontains=query, brand__name__icontains=brand).values('name')
        else:
            models = GoodsModel.objects.filter(name__icontains=query).values('name')
        context = self.get_context_data(models)
        return context

    def search_by_block_name(self, query):
        block_names = PropertyBlockName.objects.filter(name__icontains=query).values('name')
        context = self.get_context_data(block_names)
        return context

    def search_by_property_name(self, query):
        property_names = PropertyName.objects.filter(name__icontains=query).values('name')
        context = self.get_context_data(property_names)
        return context
    
    def search_by_property_value(self, query):
        property_values = PropertyValue.objects.filter(value__icontains=query).values('value')
        context = self.get_context_data(property_values)
        return context


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