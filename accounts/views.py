from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from accounts.forms import RegisterUserForm, LoginUserForm
from django.contrib.auth.views import LoginView, LogoutView 
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
class Login(LoginView):
    authentication_form = LoginUserForm
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponsePermanentRedirect(reverse_lazy('goods'))
        return super().dispatch(request, *args, **kwargs)

class Register(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('goods')
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponsePermanentRedirect(reverse_lazy('goods'))
        return super().dispatch(request, *args, **kwargs)

class Logout(LogoutView ):
    template_name = None
    next_page = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)