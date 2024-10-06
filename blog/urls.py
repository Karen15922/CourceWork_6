from django.urls import path

from blog.apps import BlogConfig
from blog.views import (PostCreateView, PostDeleteView, PostDetailView,
                        PostListView, PostUpdateView, published_toggle)

app_name = BlogConfig.name

# урлы приложения blog
urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create", PostCreateView.as_view(), name="post_create"),
    path("view/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("edit/<int:pk>", PostUpdateView.as_view(), name="post_edit"),
    path("delete/<int:pk>", PostDeleteView.as_view(), name="post_delete"),
    path("published/<int:pk>", published_toggle, name="published_toggle"),
]
