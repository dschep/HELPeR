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
    ui = {
        'background': '#f06529',
        'foreground': 'white',
        'icon': '<i class="fa fake-icon" style="font-size:50%;transform:translateY(-25%)">HTTP</i>'
    }
