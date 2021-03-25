from django.db import models
import datetime


def time_in_between(delta):
    delta_in_seconds = delta.seconds
    delta_in_hours = divmod(delta_in_seconds, 3600)[0]
    delta_in_mins = divmod(delta_in_seconds, 60)[0]

    if delta.days > 0:
        return f'{delta.days}d'
    elif delta_in_hours > 0:
        return f'{delta_in_hours}h'
    elif delta_in_mins > 0:
        return f'{delta_in_mins}m'
    else:
        return f'{delta_in_seconds}s'


class Person(models.Model):
    name = models.CharField(max_length=256)
    id = models.CharField(primary_key=True, max_length=256)
    avatar_url = models.URLField(null=True, max_length=1024)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(null=True)
    content_html = models.CharField(max_length=16384)

    def __str__(self):
        return self.content_html

    @property
    def formatted_date_modified(self):
        return self.date_modified.strftime('%m/%d/%Y %H:%M')

    @property
    def formatted_date_created(self):
        return self.date_created.strftime('%m/%d/%Y %H:%M')

    @property
    def is_updated(self):
        return not self.date_modified == self.date_created

    @property
    def time_after_posted(self):
        return time_in_between(self.date_created - self.post_set.first().date_created)

    @property
    def time_before_updated(self):
        return time_in_between(self.date_modified - self.date_created)


class PollChoice(models.Model):
    choice = models.CharField(max_length=256)
    ballots = models.ManyToManyField(Person)
    choice_image_file = models.FileField(null=True)

    def __str__(self):
        return self.choice


class Poll(models.Model):
    choices = models.ManyToManyField(PollChoice)

    def __str__(self):
        return ', '.join(map(str, self.choices.all()))


class Link(models.Model):
    url = models.URLField(max_length=1024)
    preview_text = models.CharField(max_length=16384, null=True)
    preview_image_url = models.URLField(null=True, max_length=1024)

    def __str__(self):
        if self.preview_text:
            return self.preview_text
        return self.url


class Media(models.Model):
    media_file = models.FileField(null=True)


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
    text = models.CharField(max_length=32768, null=True)
    link = models.ForeignKey(Link, null=True, on_delete=models.CASCADE)
    media = models.ManyToManyField(Media)
    id = models.CharField(max_length=256, primary_key=True)

    def __str__(self):
        if self.text:
            return self.text
        if self.link:
            return str(self.link)
        return self.content_html

    def is_public(self):
        return 'Public' in self.audience_html or '公開'

    @property
    def time_before_gp_closed(self):
        return (datetime.datetime(2019, 4, 2, tzinfo=datetime.timezone.utc) - self.date_created).days

    def formatted_date_created(self):
        return self.date_created.strftime('%m/%d/%Y %H:%M')

    def formatted_date_modified(self):
        return self.date_modified.strftime('%m/%d/%Y %H:%M')

    def is_updated(self):
        return not self.date_modified == self.date_created

    def time_before_updated(self):
        return time_in_between(self.date_modified - self.date_created)




