from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from mailings.forms import StyleFormMixin
from django import forms
from users.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'pantronymic', 'password1', 'password2')


class UserProfileForm(UserChangeForm, StyleFormMixin):
    """
    Форма профиля пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'pantronymic',
                  'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class PasswordForm(PasswordResetForm):
    """
    Форма сброса пароля
    """

    class Meta:
        model = User
        fields = ('email',)
