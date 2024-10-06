from django import forms
from django.contrib.auth.forms import (PasswordResetForm, UserChangeForm,
                                       UserCreationForm)


from mailings.forms import StyleFormMixin
from users.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class UserProfileForm(UserChangeForm, StyleFormMixin):
    """
    Форма профиля пользователя
    """

    class Meta:
        model = User
        fields = ("email", "phone", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()


class PasswordForm(PasswordResetForm):
    """
    Форма сброса пароля
    """

    class Meta:
        model = User
        fields = ("email",)

class UserForm(forms.ModelForm, StyleFormMixin):

       class Meta:
            model = User
            fields = ["email", "is_active" ]
