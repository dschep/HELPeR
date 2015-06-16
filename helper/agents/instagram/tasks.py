import os

import requests
from celery import shared_task

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup


def _check_photos(access_token, paginate=False, extra_params=None,
                  url=None, taskname=None, task_pair_id=None):
    params = {'access_token': access_token}
    if extra_params is not None:
        params.update(extra_params)

    while True:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        for image in resp.json()['data']:
            yield {
                'name': ''.join(c for c in ('' if not image['caption']
                                            else image['caption']['text'])
                                if c != os.path.sep)[:75],
                'image': image['images']['standard_resolution']['url'],
                'date': image['created_time'],
                'id': image['id'],
            }

        if 'next_max_id' in resp.json()['pagination'] and paginate:
            params['max_id'] = resp.json()['pagination']['next_max_id']
        else:
            break

@dedup('id')
@schedule(5)
@shared_task
def check_uploaded_photos(access_token, paginate=False, task_pair_id=None, **extra_agent_config):
    """
    Check Instagram for uploaded photos

    There are no configuration options

    Emits messages with the following keys: name, image, date, id
    """
    return list(_check_photos(access_token, paginate,
                              url='https://api.instagram.com/v1/users/self/media/recent',
                              taskname='check_uploaded_photos'))
check_uploaded_photos.event_keys = ['name', 'image', 'date', 'id']

@dedup('id')
@schedule(5)
@shared_task
def check_liked_photos(access_token, paginate=False, task_pair_id=None, **extra_agent_config):
    """
    Check Instagram for uploaded photos

    There are no configuration options

    Emits messages with the following keys: name, image, date, id
    """
    return list(_check_photos(access_token, paginate,
                              url='https://api.instagram.com/v1/users/self/media/liked',
                              taskname='check_uploaded_photos'))
check_liked_photos.event_keys = ['name', 'image', 'date', 'id']
