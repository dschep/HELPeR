import feedparser
from celery import shared_task

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup



@schedule(1)
@dedup('id')
@shared_task
def get_rss_feed(url, task_pair_id):
    resp = feedparser.parse(url)
    assert 'bozo_exception' not in resp
    return [{
        'title': entry.title,
        'link': entry.link,
        'description': entry.description,
        'published': entry.get('published', ''),
        'updated': entry.get('updated', ''),
        'id': entry.id,
    } for entry in resp.entries]
get_rss_feed.options = ['url']
get_rss_feed.event_keys = ['title', 'link', 'description', 'published', 'id']
