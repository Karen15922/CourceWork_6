from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from mailings.forms import MailingForm, MessageForm, ClientForm
from mailings.models import Mailing, Message, Client
from django.urls import reverse_lazy, reverse
from mailings.services import get_items_from_cache


class MailingView(TemplateView):
    template_name = 'mailings/mailings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['mailings_number'] = len(
            get_items_from_cache('mailing', Mailing, user))
        context['message_number'] = len(
            get_items_from_cache('message', Message, user))
        context['clients_number'] = len(
            get_items_from_cache('client', Client, user))
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания новой рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

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
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        """
        Добавляет исходные данные формы из GET-параметра
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs["initial"]["message"] = self.request.GET.get("id")
        form_kwargs["user"] = self.request.user
        return form_kwargs
    # def get_success_url(self):
    #     return (reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')]))

    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']

    #     if form.is_valid() and formset.is_valid():
    #         mailing = form.save()
    #         mailing.owner = self.request.user
    #         mailing.save()
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form, formset=formset))

    # def get_form_class(self):
    #     user = self.request.user
    #     if self.request.user.is_superuser:
    #         return ProductForm
    #     if user.has_perm('catalog.change_product') or self.object.owner == user:
    #         return ModeratorProductForm
    #     raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка рассылок
    """
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['mailings'] = get_items_from_cache('mailing', Mailing, user)
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения продукта
    """
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(mailing=self.object.pk)
        return context


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления продукта
    """
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


# class ContactsPageView(TemplateView):
#     """
#     контроллер для страницы контактов
#     """
#     template_name = 'catalog/contacts.html'

#     def post(self, request):
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'{name} ({phone}) "{message}"')
#         return render(request, 'catalog/contacts.html')

class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания новой рассылки
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    контроллер для страницы редактирования рассылки
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка рассылок
    """
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['messages'] = get_items_from_cache('message', Message, user)
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения продукта
    """
    model = Message


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления продукта
    """
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    контроллер для страницы создания новой рассылки
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    контроллер для страницы редактирования рассылки
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientListView(LoginRequiredMixin, ListView):
    """
    контроллер для страницы отображения списка рассылок
    """
    model = Client
    # def get_queryset(self):
    #     return get_products_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['clients'] = get_items_from_cache('clients', Client, user)
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    контроллер для страницы детального отображения продукта
    """
    model = Client


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    """
    контроллер для страницы подтверждения удаления продукта
    """
    model = Client
    success_url = reverse_lazy('mailings:client_list')
