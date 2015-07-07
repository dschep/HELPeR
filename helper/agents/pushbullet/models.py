from django import forms

from helper.models import Agent
from . import tasks


class PushbulletAgent(Agent):
    """
    <p>
    Enter your Access token from <a target="_blank"
        href="https://www.pushbullet.com/#settings/account">
        https://www.pushbullet.com/#settings/account</a> below.
    </p>
    """
    user_config_options = {
        'access_token': forms.CharField(),
    }
    effect_tasks = {
        'send_note': tasks.send_note,
        'send_link': tasks.send_link,
    }
    ui = {
        'background': '#4ab367',
        'foreground': 'white',
        'icon': '<i class="fa">PB</i>'
    }
