from django.contrib import admin

from .models import Person, Comment, Post

admin.site.register(Person)
admin.site.register(Comment)
admin.site.register(Post)
