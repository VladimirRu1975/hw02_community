from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group
from .models import Post


def index(request):

    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    context = {
        'title': 'Все посты группы',
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts = Post.objects.filter(author=username).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Страница пользователя'
    context = {
        'author': User.objects.get(username=username),
        'posts': posts,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        if request.user != post.author:
            return post_detail(request, post_id)
        form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{post.author}')
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)