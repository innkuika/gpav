from django.core.management.base import BaseCommand, CommandError
from gpav_app.models import Post, Person, Comment
import os
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Import from google plus takeout archive folder'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        posts_path = os.path.join(options['path'], 'Google+ Stream','Posts')
        for filename in os.listdir(posts_path):
            if filename.endswith('.html'):
                self.import_post(os.path.join(posts_path, filename))

    def import_post(self, post_path):
        with open(post_path) as f:
            soup = BeautifulSoup(f.recad(), 'html.parser')
            main_content_div = soup.find(name='div', class_='main-content')
            content_tags = [main_content_div] + list(main_content_div.next_siblings)
            print(''.join(map(str, content_tags)))
