from users.models import User
from mailings.models import Client, Mailing, Message
import random
from django.conf import settings
from django.core.cache import cache


def get_items_from_cache(item, model, user):
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
