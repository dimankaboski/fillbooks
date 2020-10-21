from django.shortcuts import render
from django.views.generic import ListView
from main.models import Goods


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
            brand = self.request.GET.get["brand"].split('-')
            model = self.request.GET.get["model"].split('-')
            status = self.request.GET.get["status"].split('-')
            if brand:
                queryset = queryset.filter(brand__in=brand)
            if model:
                queryset = queryset.filter(model__in=model)
            if status:
                queryset = queryset.filter(status__in=status)
            return queryset
        return super(GoodsListView, self).get_queryset()
    

def login(request):
    return render(request, 'login.html', context={})