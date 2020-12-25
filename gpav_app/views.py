from .models import Post
from django.shortcuts import render, get_object_or_404, get_list_or_404


def index(request):
    # TODO; gai hui lai
    posts = get_list_or_404(Post.objects.order_by('-date_created'))[200: 300]
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)


def post(request, post_id):
    p = get_object_or_404(Post, id=post_id)
    context = {
        'post': p,
        'comments': p.comments.all(),
        'plus_oners': ', '.join(map(lambda pp: pp.name, p.plus_oners.all())),
        'resharers': ', '.join(map(lambda pp: pp.name, p.resharers.all()))
    }
    return render(request, 'post.html', context)
