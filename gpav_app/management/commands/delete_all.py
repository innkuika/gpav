from django.core.management.base import BaseCommand
from gpav_app.models import Post, Person, Comment, Poll, PollChoice, Link, Media
import boto3
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()
        Person.objects.all().delete()
        Comment.objects.all().delete()
        Poll.objects.all().delete()
        PollChoice.objects.all().delete()
        Link.objects.all().delete()
        Media.objects.all().delete()

        # empty s3 bucket
        s3 = boto3.resource('s3')
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
