from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from accounts.forms import RegisterUserForm, LoginUserForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, BranchAddForm, PositionAddForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView ,PasswordResetDoneView, PasswordResetCompleteView 
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
class Login(LoginView):
    authentication_form = LoginUserForm
    template_name = 'login.html'


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
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


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'password_change_done.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class PasswordChange(PasswordChangeView):
    template_name = 'password_change.html'
    form_class = CustomPasswordChangeForm
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class PasswordReset(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = CustomPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


class BranchAdd(CreateView):
    form_class = BranchAddForm
    success_url = reverse_lazy('goods')
    template_name = 'add_branch.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponsePermanentRedirect(reverse_lazy('goods'))
        return super().dispatch(request, *args, **kwargs)


class PositionAdd(CreateView):
    form_class = PositionAddForm
    success_url = reverse_lazy('goods')
    template_name = 'add_position.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponsePermanentRedirect(reverse_lazy('goods'))
        return super().dispatch(request, *args, **kwargs)