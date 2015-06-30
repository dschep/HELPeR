from django import forms
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
def send_note(data, access_token, task_pair_id, title, body):
    kwargs = {'type': 'note', 'title': title, 'body': body}
    send_push(data, access_token, task_pair_id, **kwargs)
send_note.options = {
    'title': forms.CharField(label='Title'),
    'body': forms.CharField(label='Body', widget=forms.Textarea())
}

@shared_task
def send_link(data, access_token, task_pair_id, title, body, url):
    kwargs = {'type': 'link', 'title': title, 'body': body, 'url': url}
    send_push(data, access_token, task_pair_id, **kwargs)
send_link.options = {
    'title': forms.CharField(label='Title'),
    'body': forms.CharField(label='Body', widget=forms.Textarea()),
    'url': forms.CharField(label='URL'),
}


@shared_task
def send_upload_file(data, access_token=None, task_pair_id=None, **kwargs):
    raise NotImplementedError
