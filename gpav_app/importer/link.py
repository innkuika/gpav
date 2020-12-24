from gpav_app.models import Link
from typing import Optional


def import_link(soup) -> Optional[Link]:
    link_div = soup.find('a', class_='link-embed')
    if not link_div:
        return None
    link_url = link_div['href']
    link_preview_text = link_div.find('h3').text if link_div.find('h3') else None
    link_preview_image_url = link_div.find('img')['src'] if link_div.find('img') else None

    link = Link(url=link_url, preview_text=link_preview_text, preview_image_url=link_preview_image_url)
    link.save()

    return link
