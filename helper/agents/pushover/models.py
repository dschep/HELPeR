from django import forms

from helper.models import Agent
from . import tasks


class PushbulletAgent(Agent):
    """
    <p>
    Create a new Pushover application at <a target="_blank"
        href="https://pushover.net/apps/build">
        https://pushover.net/apps/build</a>.
    </p>
    <p>
    Enter your API token and user key below.
    </p>
    """
    user_config_options = {
        'token': forms.CharField(),
        'user': forms.CharField(),
    }
    effect_tasks = {
        'send_notification': tasks.send_push,
    }
    ui = {
        'background': '#3993d1',
        'foreground': 'white',
        'icon': '<i class="fa fake-icon">P</i>'
    }
