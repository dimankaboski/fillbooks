from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from main.views import GoodsListView, CheckBrand, CheckStatus, CheckBranch, BranchInfo, GoodView, GoodCreateView, GoodPriced, CustomerChoice, Notifications, SearchByQuery
from . import views


urlpatterns = [
    path('goods', GoodsListView.as_view(), name='goods'),
    path('good_create', GoodCreateView.as_view(), name='good_create'),
    path('good_card/<str:good_id>', GoodView.as_view(), name='good_card'),
    path('api/check_brand', CheckBrand.as_view(), name='check_brand'),
    path('api/check_status', CheckStatus.as_view(), name='check_status'),
    path('api/check_branch', CheckBranch.as_view(), name='check_branch'),
    path('api/branch_info', BranchInfo.as_view(), name='branch_info'),
    path('api/good_priced', GoodPriced.as_view(), name='good_priced'),
    path('api/customer_choice', CustomerChoice.as_view(), name='customer_choice'),
    path('api/get_notifications', Notifications.as_view(), name='get_notifications'),
    path('api/search_by_query', SearchByQuery.as_view(), name='search_by_query')
]
