from django import forms

from helper.models import Agent
from . import tasks


class GithubAgent(Agent):
    """
    <p>
    Then create a new personal access token at <a
    target="_blank"
    href="https://github.com/settings/tokens/new">https://github.com/settings/tokens/new</a>
    and enter it below.
    </p>
    """
    user_config_options = {
        'user': forms.CharField(),
        'access_token': forms.CharField(),
    }
    cause_tasks = {'get_notifications': tasks.get_notifications}
    ui = {
        'background': 'grey',
        'foreground': 'black',
        'icon': '<i class="fa fa-github"></i>'
    }
