import os
import requests
from django.core.files.base import ContentFile
import hashlib
from gpav_app.models import Media
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Tuple


def get_media_data(rel_path_or_url, post_path) -> Optional[Tuple[str, bytes]]:
    if rel_path_or_url.startswith("http"):
        try:
            return str(hashlib.md5(rel_path_or_url.encode("utf-8")).hexdigest()), requests.get(rel_path_or_url).content
        except requests.exceptions.ConnectionError as e:
            print(f"Error trying to get media data {rel_path_or_url}")
            print(str(e))
            return None
    else:
        media_path = os.path.normpath(os.path.join(os.path.split(post_path)[0], rel_path_or_url))
        if not os.path.exists(media_path):
            print(f"Local media does not exist {media_path}")
            return None
        with open(media_path, 'rb') as f:
            return str(hashlib.md5(media_path.encode("utf-8")).hexdigest()), f.read()


def import_media(content_html, post_path) -> List[Media]:
    soup = BeautifulSoup(content_html, 'html.parser')
    media_list = []
    for media_link in soup.find_all('a', class_='media-link'):
        media_data = get_media_data(unquote(media_link['href']), post_path)
        if not media_data:
            continue
        media = Media()
        media.media_file.save(media_data[0], ContentFile(media_data[1]))
        media.save()
        media_list.append(media)
    return media_list
