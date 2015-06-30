from django import forms

from helper.models import Agent
from . import tasks


class HttpAgent(Agent):
    """
    <p>
    This agent has no config options.
    </p>
    """
    effect_tasks = {'http_request': tasks.http_request,
                    'http_request_urldownload': tasks.http_request_urldownload}
