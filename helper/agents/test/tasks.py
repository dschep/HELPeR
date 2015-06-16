import json
import os
from pprint import pprint

import requests
from celery import shared_task


@shared_task
def get_fixtures(fixtures=None, task_pair_id=None):
    return json.loads(fixtures)
get_fixtures.event_keys = []


@shared_task
def send_print(data, fmt=None, task_pair_id=None):
    if fmt is not None:
        print(fmt.format(**data))
    else:
        print(data)


@shared_task
def send_pprint(data, task_pair_id=None):
    pprint(data)


@shared_task
def send_download_url_to_filesystem(data, url_key='url', path='.',
                                    name_fmt=None, task_pair_id=None):
    file_path = os.path.join(path, name_fmt.format(**data))
    with open(file_path, 'wb') as out:
        resp = requests.get(data[url_key], stream=True)
        resp.raise_for_status()
        for chunk in resp.iter_content(1024):
            out.write(chunk)
