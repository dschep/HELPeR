from celery import shared_task
import requests


@shared_task
def send_push(data, access_token=None, task_pair_id=None, **kwargs):
    resp = requests.post(
        'https://api.pushbullet.com/v2/pushes', auth=(access_token, ''),
        data={k: v.format(**data) for k, v in kwargs.items()},
    )
    resp.raise_for_status()


@shared_task
def send_upload_file(data, access_token=None, task_pair_id=None, **kwargs):
    raise NotImplementedError
