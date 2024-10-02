from django.contrib import admin
from mailings.models import Mailing, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'next_date', 'status')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
