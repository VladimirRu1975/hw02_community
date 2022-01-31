from django.shortcuts import get_object_or_404, render

from .models import Group
from .models import Post


def index(request):

    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'text': 'Последние обновления на сайте',
        'posts': posts,
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
