from .models import Post
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView


class PostListView(ListView):
    model = Post
    paginate_by = 50
    ordering = '-date_created'
    template_name = 'index.html'


def post(request, post_id):
    p = get_object_or_404(Post, id=post_id)
    context = {
        'post': p,
        'comments': p.comments.all(),
        'plus_oners': ', '.join(map(lambda pp: pp.name, p.plus_oners.all())),
        'resharers': ', '.join(map(lambda pp: pp.name, p.resharers.all()))
    }
    return render(request, 'post.html', context)
