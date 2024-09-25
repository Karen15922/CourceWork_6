from unicodedata import category
from urllib import request
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.db.models.base import Model
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from store.models import Category, Product, Views
from users.models import User


class ProductListView(ListView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductCreateView(CreateView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs['pk']
        product = queryset.filter(pk=pk).first()
        category = product.category
        user = self.request.user
        if Views.objects.all().filter(category=category, user=user):
            pass
        else:
            Views.objects.create(category=category, user=user)
        return queryset


class ProductUpdateView(UpdateView):
    model = Product
    success_url = reverse_lazy('store:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('store:product_list')
