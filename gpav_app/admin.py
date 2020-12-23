from django.contrib import admin

from .models import Person, Comment, Post, Poll, PollChoice

admin.site.register(Person)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Poll)
admin.site.register(PollChoice)
