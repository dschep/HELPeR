import requests
from celery import shared_task

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup


@dedup('id')
@schedule(1)
@shared_task
def get_notifications(access_token, user, task_pair_id):
    resp = requests.get('https://api.github.com/notifications',
                        auth=(user, access_token))
    resp.raise_for_status()

    events = []
    for notification in resp.json():
        events.append({
            'title': notification['subject']['title'],
            'url': notification['subject']['url'],
            'repo': notification['repository']['full_name'],
            'id': notification['id'],
        })
    return events
