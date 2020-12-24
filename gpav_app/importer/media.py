import os
import requests
from gpav_app.models import Media
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import unquote


def get_media_data(rel_path_or_url, post_path) -> Optional:
    if rel_path_or_url.startswith("http"):
        return requests.get(rel_path_or_url).content
    else:
        media_path = os.path.normpath(os.path.join(os.path.split(post_path)[0], rel_path_or_url))
        if not os.path.exists(media_path):
            print(f"Local media does not exist {media_path}")
            return None
        with open(media_path, 'rb') as f:
            return f.read()


def import_media(content_html, post_path) -> List[Media]:
    soup = BeautifulSoup(content_html, 'html.parser')
    media_list = []
    for media_link in soup.find_all('a', class_='media-link'):
        media_data = get_media_data(unquote(media_link['href']), post_path)
        if not media_data:
            continue
        media = Media(media_data=media_data)
        media.save()
        media_list.append(media)
    return media_list