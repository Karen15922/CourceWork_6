from django.forms import ModelForm, BooleanField
from mailings.models import Mailing, Message, Client


class StyleFormMixin:
    """
    класс-миксин для стилизации форм
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-checked-input"
            else:
                field.widget.attrs['class'] = "form-control"


class MailingForm(StyleFormMixin, ModelForm):
    """
    форма для создания и редактирования рассылки
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields["clients"].queryset = Client.objects.filter(
                owner=user)
            self.fields["message"].queryset = Message.objects.filter(
                owner=user)

    class Meta:
        model = Mailing
        exclude = ['owner']


class MessageForm(StyleFormMixin, ModelForm):
    """
    форма для создания и редактирования сообщения
    """
    class Meta:
        model = Message
        exclude = ['owner']


class ClientForm(StyleFormMixin, ModelForm):
    """
    форма для создания и редактирования клиента
    """
    class Meta:
        model = Client
        exclude = ['owner']
