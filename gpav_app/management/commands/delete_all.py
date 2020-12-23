from django.core.management.base import BaseCommand
from gpav_app.models import Post, Person, Comment, Poll, PollChoice


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()
        Person.objects.all().delete()
        Comment.objects.all().delete()
        Poll.objects.all().delete()
        PollChoice.objects.all().delete()