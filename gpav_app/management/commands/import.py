from django.core.management.base import BaseCommand, CommandError
from gpav_app.models import Post, Person, Comment
import os
from typing import List
from bs4 import BeautifulSoup


def import_post_author(soup) -> Person:
    author_link = soup.find('a', class_='author')
    name = author_link.span.text
    _id = author_link['href'].replace('https://plus.google.com/', '')
    avatar_url = soup.find(class_='author-photo')['src']

    p = Person(name=name, id=_id, avatar_url=avatar_url)
    print(p.name, p.id, p.avatar_url)
    # p.save()

    return p


def import_comments(soup) -> List[Comment]:
    comment_divs = soup.find_all('div', class_='comment')
    for comment_div in comment_divs:
        # parse comment author
        author_link = comment_div.find('a', class_='author')
        

        pass


def import_post(post_path):
    with open(post_path) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        # parse post author
        import_post_author(soup)

        # parse content html
        main_content_div = soup.find(name='div', class_='main-content')
        content_tags = [main_content_div] + list(main_content_div.next_siblings)
        content_html = ''.join(map(str, content_tags))

        # parse comments
        comments = import_comments(soup)


class Command(BaseCommand):
    help = 'Import from google plus takeout archive folder'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        posts_path = os.path.join(options['path'], 'Google+ Stream', 'Posts')
        for filename in os.listdir(posts_path):
            if filename.endswith('.html'):
                import_post(os.path.join(posts_path, filename))
