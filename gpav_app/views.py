from .models import Post, Media
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse
from .settings import SHOW_PRIVATE_POSTS
from django.db.models import Q


class PostListView(ListView):
    # TODO: audience_html__contains='Public' duplicates with is_public
    queryset = Post.objects.all() if SHOW_PRIVATE_POSTS else Post.objects.filter(
        Q(audience_html__contains='Public') | Q(audience_html__contains='公開'))
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


def media(request, media_id):
    m = get_object_or_404(Media, id=media_id).media_data
    return HttpResponse(str(m), 'image/jpeg')
