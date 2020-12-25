from django.urls import path

from .views import PostListView, post

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<int:post_id>', post, name='post')
]
