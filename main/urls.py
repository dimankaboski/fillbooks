from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from main.views import GoodsListView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('goods', GoodsListView.as_view(), name='goods'),
    path('login', views.login, name='login'),
]
