from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm



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
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs['class'] = 'login_input'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs['class'] = 'login_input'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'