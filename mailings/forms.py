from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError
from mailings.models import Mailing, Message
from store.forms import StyleFormMixin


class MailingForm(StyleFormMixin, ModelForm):
    """
    форма для создания и редактирования рассылки
    """
    class Meta:
        model = Mailing
        fields = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    """
    форма для создания и редактирования сообщения
    """
    class Meta:
        model = Message
        fields = '__all__'
