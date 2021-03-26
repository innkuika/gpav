from django.core.files.base import ContentFile

from gpav_app.models import Poll, PollChoice
from typing import Optional
from urllib.parse import unquote
from .person import create_person_if_absent
from .media import get_media_data


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
            image_data = get_media_data(unquote(choice_image_img['src']), post_path)

        choice = PollChoice(choice=choice)
        if image_data:
            choice.choice_image_file.save(image_data[0], ContentFile(image_data[1]))
        choice.save()
        choice.ballots.set(ballots)
        choice.save()

        choices.append(choice)

    poll = Poll()
    poll.save()
    poll.choices.set(choices)
    poll.save()

    return poll
