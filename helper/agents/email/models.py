from django import forms

from helper.models import Agent
from helper.utils.models import OAuthAgentMixin
from . import tasks


class EmailAgent(Agent):
    """
    <p>
    This agent has no config options, but ensure Django is configured to
    send email.
    </p>
    """
    effect_tasks = {'send_email': tasks.send_email}
    ui = {
        'background': 'yellow',
        'foreground': 'black',
        'icon': '<i class="fa fa-envelope-o"></i>'
    }
