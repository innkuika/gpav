from django.core.management.base import BaseCommand
from gpav_app.models import Post, Person, Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Person.objects.all().delete()
