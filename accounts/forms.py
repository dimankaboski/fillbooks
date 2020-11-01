from accounts.models import User, Branch
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm



# Допиливаем форму добавления пользователя. В Meta.model указываем нашу модель.
# Поля указывать нет необходимости т.к. они переопределяются в UserAdmin.add_fieldsets 
class RegisterUserForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'middle_name', 'email', 'branch', 'position', 'is_staff', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs['class'] = 'register-input'        
        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].widget.attrs['class'] = 'register-input'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].widget.attrs['class'] = 'register-input'
        self.fields['middle_name'].label = 'Отчество'
        self.fields['middle_name'].widget.attrs['class'] = 'register-input'
        self.fields['email'].label = 'e-mail'
        self.fields['email'].widget.attrs['class'] = 'register-input'
        self.fields['branch'].label = 'Филиал'
        self.fields['branch'].widget.attrs['class'] = 'register-input'
        self.fields['position'].label = 'Должность'
        self.fields['position'].widget.attrs['class'] = 'register-input'
        self.fields['is_staff'].label = 'Права администратора'
        self.fields['is_staff'].widget.attrs['class'] = 'register-input'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget.attrs['class'] = 'register-input'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].widget.attrs['class'] = 'register-input'
        self.error_messages['duplicate_username']='Такой логин уже существует'
        

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])



# Допиливаем форму редактирования пользователя. В Meta.model указываем нашу модель.
class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        print('da')
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs['class'] = 'login_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs['class'] = 'login_input'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['old_password'].widget.attrs['class'] = 'login_input'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Введите старый пароль'
        self.fields['new_password1'].label = 'Новый Пароль'
        self.fields['new_password1'].widget.attrs['class'] = 'login_input'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Введите новый пароль'
        self.fields['new_password2'].label = 'Новый пароль еще раз'
        self.fields['new_password2'].widget.attrs['class'] = 'login_input'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Введите новый пароль'

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'e-mail'
        self.fields['email'].widget.attrs['class'] = 'login_input'
        self.fields['email'].widget.attrs['placeholder'] = 'email для восстановления'

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новый Пароль'
        self.fields['new_password1'].widget.attrs['class'] = 'login_input'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Введите новый пароль'
        self.fields['new_password2'].label = 'Новый пароль еще раз'
        self.fields['new_password2'].widget.attrs['class'] = 'login_input'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Введите новый пароль'

class BranchAddForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BranchAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'register-input'
        self.fields['name'].widget.attrs['placeholder'] = 'Название филиала'
        self.fields['address'].widget.attrs['class'] = 'register-input'
        self.fields['address'].widget.attrs['placeholder'] = 'Адрес филиала'
        self.fields['balance'].widget.attrs['class'] = 'register-input'
        self.fields['balance'].widget.attrs['placeholder'] = 'Баланс филиала'


class PositionAddForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PositionAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'register-input'
        self.fields['name'].widget.attrs['placeholder'] = 'Название филиала'
