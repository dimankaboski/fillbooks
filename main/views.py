from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', context={})

def goods(request):
    return render(request, 'goods.html', context={})

def login(request):
    return render(request, 'login.html', context={})