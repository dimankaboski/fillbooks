from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import Register, Login, Logout


urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    # path('password_change/', name='password_change'),
    # path('password_change/done/', name='password_change_done'),
    # path('password_reset/', name='password_reset'),
    # path('password_reset/done/', name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', name='password_reset_confirm'),
    # path('reset/done/', name='password_reset_complete'),
]
