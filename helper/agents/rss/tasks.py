import time
import datetime

import feedparser
from celery import shared_task
from django import forms

from helper.scheduler import schedule
from helper.utils.decorators import dedup, format_options_from_event
from helper.agents.utils import send_to_event_store

def struct2isoformat(struct):
    if struct is None:
        return ''
    return datetime.datetime.fromtimestamp(time.mktime(struct)).isoformat()


@schedule(1)
@dedup('id')
@shared_task
def get_rss_feed(url, task_pair_id, secret):
    resp = feedparser.parse(url)
    assert 'bozo_exception' not in resp
    return [{
        'title': entry.title,
        'link': entry.link,
        'description': entry.description,
        'published': ('' if 'published_parsed' not in entry
                      else struct2isoformat(entry.published_parsed)),
        'updated': ('' if 'updated_parsed' not in entry
                    else struct2isoformat(entry.updated_parsed)),
        'id': entry.id,
    } for entry in resp.entries]
get_rss_feed.options = {'url': forms.URLField(label='URL')}
get_rss_feed.event_keys = ['title', 'link', 'description', 'published', 'id']
get_rss_feed.label = 'Get feed'


@shared_task
@format_options_from_event
def generate_rss_feed(data, task_pair_id, **kwargs):
    send_to_event_store(kwargs, task_pair_id, 'effect')
generate_rss_feed.options = {
    'feed_title': forms.CharField(label='Feed title'),
    'feed_link': forms.CharField(label='Feed link'),
    'feed_description': forms.CharField(label='Feed description'),
    'item_title': forms.CharField(label='Item title'),
    'item_link': forms.CharField(label='Item link'),
    'item_description': forms.CharField(label='Item description'),
    'item_guid': forms.CharField(label='Item GUID'),
    'item_pubdate': forms.CharField(label='Item publication date'),
}
generate_rss_feed.label = 'Generate feed'
