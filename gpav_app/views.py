from .models import Post, Media
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse
from .settings import SHOW_PRIVATE_POSTS
from django.db.models import Q


class PostListView(ListView):
    paginate_by = 25
    template_name = 'index.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        posts = Post.objects.all()

        if not SHOW_PRIVATE_POSTS:
            # TODO: audience_html__contains='Public' duplicates with is_public
            posts = posts.filter(Q(audience_html__contains='Public') | Q(audience_html__contains='公開'))

        if q != '':
            posts = posts.filter(Q(text__contains=q) | Q(plus_oners__name__contains=q) | Q(resharers__name__contains=q)
                                 | Q(comments__content_html__contains=q) | Q(comments__author__name__contains=q))
        return posts.order_by('-date_created').distinct()


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
