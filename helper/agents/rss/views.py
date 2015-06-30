import datetime
from io import StringIO

from django.http import HttpResponse

import PyRSS2Gen

from helper.agents.utils import get_from_event_store


def generate_rss_feed(request, task_pair):
    rss = PyRSS2Gen.RSS2(
        title=task_pair.effect_options['feed_title'],
        link=task_pair.effect_options['feed_link'],
        description=task_pair.effect_options['feed_description'],
        lastBuildDate=datetime.datetime.now(),
        items=[PyRSS2Gen.RSSItem(
            title=event['item_title'],
            link=event['item_link'],
            description=event['item_description'],
            guid=PyRSS2Gen.Guid(event['item_guid']),
            pubDate=datetime.datetime.strptime(event['item_pubdate'][:19],
                                                '%Y-%m-%dT%H:%M:%S')
        ) for event in get_from_event_store(task_pair.id, 'effect')]
    )
    strio = StringIO()
    rss.write_xml(strio)
    strio.seek(0)

    return HttpResponse(strio.read(), content_type='application/rss+xml')
