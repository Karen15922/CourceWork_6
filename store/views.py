from django.shortcuts import render, redirect
from django.db.models.base import Model
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from store.models import Category, Product, Release


class ProductListView(ListView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductCreateView(CreateView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session[f'{self.object}'] = 'test_message'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('store:product_list')
