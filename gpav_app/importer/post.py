from gpav_app.models import Post, Person, Comment
from typing import List, Optional
from bs4 import BeautifulSoup
from dateutil import parser
from .person import create_person_if_absent
from .poll import import_poll
from .link import import_link


def import_post_author(soup) -> Person:
    author_link = soup.find('a', class_='author')
    name = author_link.span.text
    _id = author_link['href'].replace('https://plus.google.com/', '')
    avatar_url = soup.find(class_='author-photo')['src']

    p = Person(name=name, id=_id, avatar_url=avatar_url)
    p.save()

    return p


def import_text(soup) -> Optional[str]:
    text_div = soup.find('span', itemprop='text')
    if not text_div:
        return None

    html = str(text_div).replace('<br>', '\n')
    new_soup = BeautifulSoup(html, 'html.parser')
    return new_soup.text


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

        # parse text
        text = import_text(soup)

        # parse link
        link = import_link(soup)

        # create post
        post = Post(author=author, date_created=date_created, date_modified=date_modified, content_html=content_html,
                    audience_html=audience_html, poll=poll, text=text, link=link)
        post.save()
        post.plus_oners.set(plus_oners)
        post.resharers.set(resharers)
        post.comments.set(comments)
        post.save()
