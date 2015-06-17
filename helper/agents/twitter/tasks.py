import json

import tweepy
from celery import shared_task

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup


def get_api(consumer_key, consumer_secret,
            access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

@shared_task
def send_tweet(data, status, task_pair_id,
               consumer_key, consumer_secret,
               access_token, access_token_secret):
    api = get_api(consumer_key, consumer_secret,
                  access_token, access_token_secret)

    api.update_status(status=status.format(**data))
send_tweet.options = ['status']


@dedup('id')
@schedule(5)
@shared_task
def sent_tweet(user, task_pair_id,
               consumer_key, consumer_secret,
               access_token, access_token_secret):
    api = get_api(consumer_key, consumer_secret,
                  access_token, access_token_secret)

    return [{
        'id': str(t.id),
        'status': t.text,
        'date': str(t.created_at),
        'raw': json.dumps(t._json),
    } for t in api.user_timeline(screen_name=user)]
sent_tweet.options = ['user']
sent_tweet.event_keys = ['id', 'status', 'date', 'raw']
