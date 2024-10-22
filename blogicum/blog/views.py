from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from blog.models import Post, Category, Comment
from .forms import UserForm, PostForm, CommentForm

User = get_user_model()


@login_required
def create_post(request):
    template = 'blog/create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect(f'/profile/{request.user.username}/')
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username
    )

    profile_posts = Post.objects.filter(author=profile)
    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if instance.author != request.user:
        return redirect(f'/posts/{post_id}/')
    template = 'blog/create.html'
    form = PostForm(
        request.POST or None,
        instance=instance,
        files=request.FILES or None
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(f'/posts/{post_id}/')
    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    template = 'blog/create.html'
    instance = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=instance)
    context = {'form': form}

    if instance.author != request.user:
        return redirect(f'/posts/{post_id}/')

    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')

    return render(request, template, context)


@login_required
def edit_profile(request):
    instance = get_object_or_404(User, pk=request.user.id)
    template = 'blog/user.html'
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect(f'/posts/{post_id}/')
    template = 'blog/comment.html'
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'form': form,
        'comment': comment
    }
    if form.is_valid():
        form.save()
        return redirect(f'/posts/{post_id}/')
    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {'comment': comment}
    if comment.author != request.user:
        return redirect(f'/posts/{post_id}/')

    if request.method == 'POST':
        comment.delete()
        return redirect(f'/posts/{post_id}/')

    return render(request, template, context)


def get_posts():
    return Post.objects.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    posts = get_posts()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=post_id
    )

    if post.author != request.user:
        post = get_object_or_404(
            get_posts(),
            pk=post_id
        )

    comments = Comment.objects.all()
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template, context)
