from datetime import datetime, timedelta
from smtplib import SMTPException

import pytz  # type: ignore
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Mailing_attempt

t_zone = pytz.timezone(settings.TIME_ZONE)


def get_items_from_cache(item, model, user, db=False):
    """
    возвращает объекты из кеша для пользователя
    """
    if db:
        return model.objects.all()
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


def get_number_of_attempts(user):
    mailings = user.mailing.all()
    attempts = Mailing_attempt.objects.all().filter(mailing__in=mailings)
    return len(attempts)


def get_active_mailings():
    """
    возвращает активные рассылки из бд
    """
    mailings = Mailing.objects.filter(status="active")
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
    except SMTPException as ex:
        Mailing_attempt.objects.create(
            mailing=mailing, smtp_service_report=ex, owner=mailing.owner
        )
    else:
        Mailing_attempt.objects.create(
            mailing=mailing, smtp_service_report="отправлено", status="success"
        )


def mailings_routine():
    """
    проводит периодические рассылки
    """
    time_adder = {
        "ежедневно": timedelta(minutes=1),
        "еженедельно": timedelta(minutes=3),
        "ежемесячно": timedelta(minutes=5),
    }

    mailings = get_active_mailings().filter(next_date__lte=datetime.now(t_zone))
    for mailing in mailings:
        send_message(mailing)
        if mailing.periodicity == "однократно":
            mailing.status = "complited"
            mailing.save(update_fields=["status"])
        else:
            mailing.next_date += time_adder[mailing.periodicity]
            mailing.save(update_fields=["next_date"])
