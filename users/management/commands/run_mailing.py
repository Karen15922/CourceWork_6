from django.core.management import BaseCommand
from mailings.services import mailings_routine
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        mailings_routine()
