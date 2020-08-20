from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .forms import PostForm
from .models import Post, Group

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST)
    if request.method != 'POST' or not form.is_valid():
        return render(request, 'new.html', {'form': form, 'type': 'new'})
    newp = form.save(commit=False)
    newp.author = request.user
    newp.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    # Пагинатор
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'profile.html',
        {
            'page': page,
            'paginator': paginator,
            'count_posts': post_list.count(),
            'author': author,
        }
    )


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)

    post = get_object_or_404(Post, id=post_id, author=author)
    cnt_posts = author.posts.count()
    return render(
        request,
        'post.html',
        {
            'count_posts': cnt_posts,
            'post': post,
            'author': author
        }
    )


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=author)

    if post.author != request.user:
        return redirect('user_post', username=username, post_id=post_id)

    form = PostForm(request.POST, instance=post)
    if request.method != 'POST' or not form.is_valid():
        return render(request, 'new.html', {'form': form, 'type': 'change', 'post': post})
    form.save()
    return redirect('user_post', username=username, post_id=post_id)
