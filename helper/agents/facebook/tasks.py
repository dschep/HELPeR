import os

import requests
from celery import shared_task

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup


def _check_photos(access_token, paginate=False, extra_params=None,
                  taskname=None, task_pair_id=None):
    params = {'access_token': access_token}
    if extra_params is not None:
        params.update(extra_params)

    while True:
        resp = requests.get('https://graph.facebook.com/me/photos',
                            params=params)
        resp.raise_for_status()
        for image in resp.json()['data']:
            yield {
                'user': image['from']['name'],
                'name': ''.join(c for c in image.get('name', '(nocaption)')
                                if c not in '?#'+os.path.sep)[:75],
                'image': image['images'][0]['source'],
                'date': image['created_time'],
                'fbid': image['id'],
            }

        if 'next' in resp.json()['paging'] and paginate:
            params['after'] = resp.json()['paging']['cursors']['after']
        else:
            break

@dedup('fbid')
@schedule(5)
@shared_task
def check_tagged_photos(access_token, paginate=False, task_pair_id=None, **extra_agent_config):
    """
    Check Facebook for tagged public photos of myself

    There are no configuration options

    Emits messages with the following keys: user, name, image, date, fbid
    """
    return list(_check_photos(access_token, paginate,
                              taskname='check_tagged_photos'))
check_tagged_photos.event_keys = ['user', 'name', 'image', 'date', 'fbid']


@dedup('fbid')
@schedule(5)
@shared_task
def check_uploaded_photos(access_token, paginate=False, task_pair_id=None, **extra_agent_config):
    """
    Check Facebook for uploaded photos

    There are no configuration options

    Emits messages with the following keys: user, name, image, date, fbid
    """
    return list(_check_photos(access_token, paginate, {'type': 'uploaded'},
                              taskname='check_uploaded_photos'))
check_uploaded_photos.event_keys = ['user', 'name', 'image', 'date', 'fbid']

#TODO: adapt post to fb from pirana. low pri bc apps need to be approved :/
#def recieve_post_to_facebook(self, event):
#    params = {'access_token': self.access_token}
#    params.update({key: value.format(**event)
#                    for key, value in self.post_args.items()})
#
#    resp = requests.post('https://graph.facebook.com/me/feed',
#                        params=params)
#    resp.raise_for_status()
#    if conf.verbose:
#        params.pop('access_token')
#        print('posted "{}" to facebook'.format(params))
#
