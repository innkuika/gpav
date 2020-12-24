import os
import requests
from gpav_app.models import Poll, PollChoice
from typing import Optional
from urllib.parse import unquote
from .person import create_person_if_absent


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
