from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailings.forms import ClientForm, MailingForm, MessageForm
from mailings.models import Client, Mailing, Mailing_attempt, Message
from mailings.services import get_items_from_cache


class MailingView(TemplateView):
    """
    контроллер приложения mailings
    """

    template_name = "mailings/mailings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["mailings_number"] = len(get_items_from_cache("mailing", Mailing, user))
        context["message_number"] = len(get_items_from_cache("message", Message, user))
        context["clients_number"] = len(get_items_from_cache("client", Client, user))
        context["attempt_number"] = len(
            get_items_from_cache("attempts", Mailing_attempt, user)
        )
        return context


class MailingLogView(TemplateView):
    """
    контроллер логов рассылок
    """

    template_name = "mailings/mailing_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["attempts"] = get_items_from_cache("attempts", Mailing_attempt, user)
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Добавляет исходные данные формы из GET-параметра
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs["initial"]["message"] = self.request.GET.get("id")
        form_kwargs["user"] = self.request.user
        return form_kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    контроллер для страницы редактирования рассылки
    """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["initial"]["message"] = self.request.GET.get("id")
        form_kwargs["user"] = self.request.user
        return form_kwargs


class MailingListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка рассылок
    """

    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["mailings"] = get_items_from_cache("mailing", Mailing, user)
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения рассылки
    """

    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(owner=self.object.pk)
        return context


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления рассылки
    """

    model = Mailing
    success_url = reverse_lazy("mailings:mailing_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания сообщения
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    контроллер для страницы редактирования сообщения
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка сообщений
    """

    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["messages"] = get_items_from_cache("message", Message, user)
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения сообщения
    """

    model = Message


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления сообщения
    """

    model = Message
    success_url = reverse_lazy("mailings:message_list")


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания клиента
    """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    контроллер для страницы редактирования клиента
    """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")


class ClientListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка клиентов
    """

    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["clients"] = get_items_from_cache("clients", Client, user)
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения клиента
    """

    model = Client


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления клиента
    """

    model = Client
    success_url = reverse_lazy("mailings:client_list")
