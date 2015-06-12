import requests
from celery import shared_task

from helper.agents.utils import send_to_event_store, get_from_event_store


#@shared_task
#def get_url_http_request(url=None, task_pair_id=None):
#    return requests.get(url)
#
#
#@shared_task
#def get_url_http_request_json(url=None, jsonpath=None, task_pair_id=None):
#    return parse_jsonpath(jsonpath).find(requests.get(url).json())


@shared_task
def send_to_view(data, **kwargs):
    return send_to_event_store(data, **kwargs)


@shared_task
def get_from_view(**kwargs):
    return get_from_event_store(**kwargs)
