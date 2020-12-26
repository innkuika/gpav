from django.urls import path

from .views import PostListView, post, media

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<str:post_id>', post, name='post'),
    path('media/<int:media_id>', media, name='media')
]
