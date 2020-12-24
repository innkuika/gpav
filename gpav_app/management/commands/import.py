import os
from django.core.management.base import BaseCommand
from gpav_app.importer.post import import_post


class Command(BaseCommand):
    help = 'Import from google plus takeout archive folder'

    def add_arguments(self, arg_parser):
        arg_parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        posts_path = os.path.join(options['path'], 'Google+ Stream', 'Posts')
        for filename in os.listdir(posts_path):
            if filename.endswith('.html'):
                import_post(os.path.join(posts_path, filename))
