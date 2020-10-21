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

def login(request):
    return render(request, 'login.html', context={})