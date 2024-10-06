from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from pytils.translit import slugify

from blog.models import Post


class PostCreateView(CreateView):
    """
    контроллер создания поста
    """

    model = Post
    fields = ("title", "content", "image")
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """
    контроллер редактирования поста
    """

    model = Post
    fields = ("title", "content", "image")
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs.get("pk")])


class PostListView(ListView):
    """
    контроллер списка постов
    """

    model = Post

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(is_published=True)


class PostDetailView(DetailView):
    """
    контроллер детального просмотра поста
    """

    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class PostDeleteView(DeleteView):
    """
    контроллер удаления поста
    """

    model = Post
    success_url = reverse_lazy("blog:post_list")


def published_toggle(request, pk):
    """
    контроллер публикации поста
    """
    post = get_object_or_404(Post, pk=pk)
    if post.is_published:
        post.is_published = False
    else:
        post.is_published = True

    post.save()
    return redirect(reverse("blog:post_list"))
