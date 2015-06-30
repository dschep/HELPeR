from collections import OrderedDict
import requests
from celery import shared_task
from django import forms

from helper.utils.decorators import format_options_from_event


@shared_task
@format_options_from_event
def send_push(data, token, user, message, title, device, url, url_title,
              priority, html, task_pair_id=None):
    resp = requests.post('https://api.pushover.net/1/messages.json', data={
        'title': title,
        'message': message,
        'token': token,
        'user': user,
        'html': html,
        'url': url,
        'url_title': url_title,
        'priority': priority,
    })
    resp.raise_for_status()
send_push.options = OrderedDict([
    ('title', forms.CharField(label='Title', required=False)),
    ('message', forms.CharField(label='Message', widget=forms.Textarea())),
    ('device', forms.CharField(label='Device', required=False)),
    ('html', forms.ChoiceField(required=False, label='HTML', choices=[
        ('1', 'True'), ('', 'False')])),
    ('url', forms.CharField(label='URL', required=False)),
    ('url_title', forms.CharField(label='URL title', required=False)),
    ('priority', forms.ChoiceField(label='Priority',
                                   choices=[(str(x),)*2 for x in range(-2, 3)])),
])
