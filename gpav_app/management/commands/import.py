import os
import requests
from django.core.management.base import BaseCommand
from gpav_app.models import Post, Person, Comment, Poll, PollChoice
from typing import List, Optional
from bs4 import BeautifulSoup
from dateutil import parser
from urllib.parse import unquote


def create_person_if_absent(person_id, name) -> Person:
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        person = Person(id=person_id, name=name)
        person.save()

    return person


def import_post_author(soup) -> Person:
    author_link = soup.find('a', class_='author')
    name = author_link.span.text
    _id = author_link['href'].replace('https://plus.google.com/', '')
    avatar_url = soup.find(class_='author-photo')['src']

    p = Person(name=name, id=_id, avatar_url=avatar_url)
    p.save()

    return p


def import_comments(soup) -> List[Comment]:
    comment_divs = soup.find_all('div', class_='comment')
    if not comment_divs:
        return []

    comments = []
    for comment_div in comment_divs:
        # parse comment author
        author_link = comment_div.find('a', class_='author')
        author_id = author_link['href'].replace('https://plus.google.com/', '')
        author_name = author_link.span.text
        author = create_person_if_absent(author_id, author_name)

        # parse comment date created
        date_created = parser.parse(comment_div.find('span', itemprop='dateCreated').text)

        # parse comment date modified
        date_modified_span = comment_div.find('span', itemprop='dateModified')
        if date_modified_span:
            date_modified = parser.parse(date_modified_span.text)
        else:
            date_modified = None

        # parse content html
        comment_content_div = comment_div.find('div', class_='comment-content')
        content_tags = [comment_content_div] + list(comment_content_div.next_siblings)
        comment_content_html = ''.join(map(str, content_tags))

        # create comment
        comment = Comment(author=author, date_created=date_created, date_modified=date_modified,
                          content_html=comment_content_html)
        comment.save()
        comments.append(comment)

    return comments


def import_persons_in_element(soup, class_) -> List[Person]:
    """
    soup: beautiful soup instance
    class_: the class of the elements to import person
    """
    plus_oners_div = soup.find('div', class_=class_)
    if not plus_oners_div:
        return []

    plus_oners = []
    for plus_oner_link in plus_oners_div.find_all('a'):
        plus_oner_id = plus_oner_link['href'].replace('https://plus.google.com/', '')
        plus_oner_name = plus_oner_link.text
        plus_oner = create_person_if_absent(plus_oner_id, plus_oner_name)
        plus_oners.append(plus_oner)

    return plus_oners


def import_poll(soup, post_path) -> Optional[Poll]:
    if not soup.find('div', class_='poll-choice'):
        return None

    # get all ballots for now
    all_ballots = []
    for ballot_link in soup.find('div', class_='poll-choice-votes').find_all('a'):
        ballot_id = ballot_link['href'].replace('https://plus.google.com/', '')
        ballot_name = ballot_link.text
        ballot = create_person_if_absent(ballot_id, ballot_name)
        all_ballots.append(ballot)

    cur_ballot_ptr = 0
    choices = []
    for choice_div in soup.find_all('div', class_='poll-choice'):
        # parse choice
        choice_description_div = choice_div.find('div', class_='poll-choice-description')
        choice = choice_description_div.text

        # parse ballots
        count = int(choice_description_div.next_sibling.text.split(' ')[0])
        ballots = all_ballots[cur_ballot_ptr: cur_ballot_ptr + count]
        cur_ballot_ptr += count

        # get image
        image_data = None
        choice_image_div = choice_div.find('div', class_='poll-choice-image')
        choice_image_img = choice_image_div.find('img')
        if choice_image_img:
            image_rel_path_or_url = unquote(choice_image_img['src'])
            if image_rel_path_or_url.startswith("http"):
                image_data = requests.get(image_rel_path_or_url).content
            else:
                image_path = os.path.normpath(os.path.join(os.path.split(post_path)[0], image_rel_path_or_url))
                with open(image_path, 'rb') as f:
                    image_data = f.read()

        choice = PollChoice(choice=choice, choice_image=image_data)
        choice.save()
        choice.ballots.set(ballots)
        choice.save()

        choices.append(choice)

    poll = Poll()
    poll.save()
    poll.choices.set(choices)
    poll.save()

    return poll


def import_post(post_path):
    print('Importing ', post_path)
    with open(post_path) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        # parse post author
        author = import_post_author(soup)

        # parse date created
        date_created = parser.parse(soup.find('span', itemprop='dateCreated').text)

        # parse comment date modified
        date_modified_span = soup.find('span', itemprop='dateModified')
        if date_modified_span:
            date_modified = parser.parse(date_modified_span.text)
        else:
            date_modified = None

        # parse content html
        main_content_div = soup.find(name='div', class_='main-content')
        content_tags = [main_content_div] + list(main_content_div.next_siblings)
        content_html = ''.join(map(str, content_tags))

        # parse audience html
        audience_html = str(soup.find(name='span', itemprop='audience'))

        # parse plus oners
        plus_oners = import_persons_in_element(soup, 'plus-oners')

        # parse resharers
        resharers = import_persons_in_element(soup, 'resharers')

        # parse comments
        comments = import_comments(soup)

        # parse poll
        poll = import_poll(soup, post_path)

        # create post
        post = Post(author=author, date_created=date_created, date_modified=date_modified, content_html=content_html,
                    audience_html=audience_html, poll=poll)
        post.save()
        post.plus_oners.set(plus_oners)
        post.resharers.set(resharers)
        post.comments.set(comments)
        post.save()


class Command(BaseCommand):
    help = 'Import from google plus takeout archive folder'

    def add_arguments(self, arg_parser):
        arg_parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        posts_path = os.path.join(options['path'], 'Google+ Stream', 'Posts')
        for filename in os.listdir(posts_path):
            if filename.endswith('.html'):
                import_post(os.path.join(posts_path, filename))
