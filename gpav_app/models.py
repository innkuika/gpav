from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=256)
    id = models.CharField(primary_key=True, max_length=256)
    avatar_url = models.URLField(null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(null=True)
    content_html = models.CharField(max_length=16384)

    def __str__(self):
        return self.content_html


class PollChoice(models.Model):
    choice = models.CharField(max_length=256)
    ballots = models.ManyToManyField(Person)
    choice_image = models.BinaryField(null=True)

    def __str__(self):
        return self.choice


class Poll(models.Model):
    choices = models.ManyToManyField(PollChoice)

    def __str__(self):
        return ', '.join(map(str, self.choices.all()))


class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='author')
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(null=True)
    content_html = models.CharField(max_length=32768)
    audience_html = models.CharField(max_length=16384)
    plus_oners = models.ManyToManyField(Person, related_name='plus_oners')
    resharers = models.ManyToManyField(Person, related_name='resharers')
    comments = models.ManyToManyField(Comment)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content_html
