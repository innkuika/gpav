from .models import Post
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.http import Http404
from .settings import SHOW_PRIVATE_POSTS


class PostListView(ListView):
    # TODO: audience_html__contains='Public' duplicates with is_public
    queryset = Post.objects.all() if SHOW_PRIVATE_POSTS else Post.objects.filter(audience_html__contains='Public')
    paginate_by = 25
    ordering = '-date_created'
    template_name = 'index.html'


def post(request, post_id):
    p = get_object_or_404(Post, id=post_id)
    if not SHOW_PRIVATE_POSTS and not p.is_public():
        raise Http404()
    context = {
        'post': p,
        'plus_oners': ', '.join(map(lambda pp: pp.name, p.plus_oners.all())),
        'resharers': ', '.join(map(lambda pp: pp.name, p.resharers.all()))
    }
    return render(request, 'post.html', context)
