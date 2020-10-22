from django.shortcuts import render
from django.views.generic import ListView
from main.models import Goods, GoodsBrand, GoodsModel


# Create your views here.
def index(request):
    return render(request, 'index.html', context={})

def goods(request):
    return render(request, 'goods.html', context={})

class GoodsListView(ListView):

    template_name = 'goods.html'
    model = Goods
    
    def get_queryset(self):
        if self.request.GET:
            queryset = Goods.objects.all()

            brand = self.request.GET.get("brand")
            model = self.request.GET.get("model")
            status = self.request.GET.get("status")
            if brand:
                brand = GoodsBrand.objects.filter(name__in=brand.split('-'))
                queryset = queryset.filter(brand__in=brand)
            if model:
                model = GoodsModel.objects.filter(name__in=model.split('-'))
                queryset = queryset.filter(model__in=model)
            if status:
                queryset = queryset.filter(status__in=status.split('-'))
            return queryset
        return super(GoodsListView, self).get_queryset()
    

def login(request):
    return render(request, 'login.html', context={})

def good_card(request):
    return render(request, 'good_card.html', context={})

def register(request):
    return render(request, 'register.html', context={})