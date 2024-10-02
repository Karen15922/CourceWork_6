from users.models import User
from mailings.models import Client, Mailing, Message
from store.models import Views, Category
import random
from django.conf import settings
from django.core.cache import cache


def get_clients():
    for view in Views.objects.all():
        if not Client.objects.filter(email=view.user.email).exists():
            Client.objects.create(first_name=view.user.first_name, last_name=view.user.last_name,
                                  pantronymic=view.user.pantronymic, email=view.user.email, comment='test')


def create_mailing():
    categories = list(Category.objects.all())
    choosed_category = random.choice(categories)
    mailing = Mailing()
    clients = Views.objects.filter(category=choosed_category)
    mailing.clients.add(*clients)
    mailing.save()


def get_items_from_cache(item, model):
    if settings.CACHES_ENABLED:
        items = cache.get(item)
        if not items:
            items = model.objects.all()
            cache.set(item, items)
    else:
        items = model.objects.all()
    return items
