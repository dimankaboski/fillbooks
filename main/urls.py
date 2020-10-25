from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from main.views import GoodsListView, CheckBrand, CheckStatus, CheckBranch, BranchInfo
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('goods', GoodsListView.as_view(), name='goods'),
    path('login', views.login, name='login'),
    path('good_card', views.good_card, name='good_card'),
    path('register', views.register, name='register'),
    path('api/check_brand', CheckBrand.as_view(), name='check_brand'),
    path('api/check_status', CheckStatus.as_view(), name='check_status'),
    path('api/check_branch', CheckBranch.as_view(), name='check_branch'),
    path('api/branch_info', BranchInfo.as_view(), name='branch_info'),
]
