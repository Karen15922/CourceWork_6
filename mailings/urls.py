from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import (
    MailingCreateView, MailingListView, MailingDetailView,
    MailingUpdateView, MailingDeleteView, MailingView,
    MessageCreateView, MessageUpdateView, MessageListView,
    MessageDetailView, MessageDeleteView,
    ClientCreateView, ClientUpdateView, ClientListView,
    ClientDetailView, ClientDeleteView)
# from django.views.decorators.cache import cache_page

app_name = MailingsConfig.name

# урлы приложения mailings
urlpatterns = [
    path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
    path('', MailingView.as_view(), name='mailings'),
    path('mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_update/<int:pk>',
         MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>',
         MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings_list', MailingListView.as_view(), name='mailing_list'),
    path('message_create', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>',
         MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>',
         MessageDeleteView.as_view(), name='message_delete'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>',
         ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>',
         ClientDeleteView.as_view(), name='client_delete'),
    path('client_list', ClientListView.as_view(), name='client_list'),
]
