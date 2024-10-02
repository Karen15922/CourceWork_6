from smtplib import SMTPException
from datetime import datetime, timedelta
from django.conf import settings
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Mailing_attempt
from django.core.mail import send_mail
from django.core.cache import cache
import pytz  # type: ignore

t_zone = pytz.timezone(settings.TIME_ZONE)


def get_items_from_cache(item, model, user):
    """
    возвращает объекты из кеша для пользователя
    """
    if settings.CACHES_ENABLED:
        items = cache.get(item)
        if not items:
            items = model.objects.all()
            cache.set(item, items)
    else:
        items = model.objects.all()
    if user.is_authenticated:
        if not user.is_superuser:
            return items.filter(owner=user)
    return items


def get_active_mailings():
    """
    возвращает активные рассылки из бд
    """
    mailings = Mailing.objects.filter(status='active')
    return mailings


def send_message(mailing):
    """
    отправляет сообщение клиентам рассылки
    """
    try:
        send_mail(
            mailing.message.title,
            mailing.message.content,
            EMAIL_HOST_USER,
            [client.email for client in mailing.clients.all()],
        )
    except SMTPException as exception:
        Mailing_attempt.objects.create(
            mailing=mailing, smtp_service_report=exception)
    else:
        Mailing_attempt.objects.create(
            mailing=mailing, smtp_sevice_report='отправлено', status='success')


def mailings_routine():
    """
    проводит периодические рассылки
    """
    time_adder = {
        'ежедневно': timedelta(minutes=1),
        'еженедельно': timedelta(minutes=3),
        'ежедневно': timedelta(minutes=5),
    }

    mailings = Mailing.objects.filter(
        status='active', next_date__lte=datetime.now(t_zone))
    for mailing in mailings:
        send_message(mailing)
        if mailing.periodicity == ['однократно']:
            mailing.status = 'complited'
            mailing.save(update_fields=['status'])
        else:
            mailing.next_date += time_adder[mailing.periodicity]
            mailing.save(update_fields=['next_date'])
