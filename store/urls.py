from django.urls import path
from store.apps import StoreConfig
from store.views import ProductListView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView

app_name = StoreConfig.name

# урлы приложения store
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create', ProductCreateView.as_view(), name='product_create'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
]
