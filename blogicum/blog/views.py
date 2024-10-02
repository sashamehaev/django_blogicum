from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Post, Category


POSTS_PER_PAGE = 5

User = get_user_model()


class BirthdayDetailView(DetailView):
    model = User


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username
    )
    print(profile)
    context = {'profile': profile}
    return render(request, template, context)


def get_posts():
    return Post.objects.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    posts = get_posts()[:POSTS_PER_PAGE]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_posts(),
        pk=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True
        ),
        slug=category_slug
    )

    posts = get_posts().filter(category__slug=category_slug)
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template, context)
