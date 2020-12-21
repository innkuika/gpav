from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=256)
    id = models.CharField(primary_key=True, max_length=256)
    avatar_url = models.URLField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    content_html = models.CharField(max_length=1024)

    def __str__(self):
        return self.content_html


class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='author')
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    content_html = models.CharField(max_length=1024)
    audience_html = models.CharField(max_length=1024)
    plus_oners = models.ManyToManyField(Person, related_name='plus_oners')
    resharers = models.ManyToManyField(Person, related_name='resharers')
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return self.content_html
