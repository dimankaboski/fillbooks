from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import *
from accounts.forms import AdminUserChangeForm, AdminUserAddForm
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    list_display = ('username','first_name', 'last_name', 'position', 'branch')
    readonly_fields =('last_login', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'branch', 'position')
    fieldsets = (
        (None, {'fields': ['username']}),
        (('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'position', 
            'branch',
            'is_admin'
        )}),
        # (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'balance')
    search_fields = ('name', 'address', 'balance')

class PositionAdmin(admin.ModelAdmin):
    list_display =['name']
    search_fields = ['name']

admin.site.register(User, UserAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Branch, BranchAdmin)