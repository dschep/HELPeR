from django import forms

from helper.models import Agent
from . import tasks


class DropboxAgent(Agent):
    """
    <p>
    Create a Dropbox API App at <a target="_blank" href="https://www.dropbox.com/developers/apps/create">https://www.dropbox.com/developers/apps/create</a>
    </p>
    <p>
    Click <strong>Generate access token</strong> in the OAuth 2 section and enter
    the generated token below.
    </p>
    """
    user_config_options = {
        'access_token': forms.CharField(),
    }
    effect_tasks = {'send_file_to_dropbox': tasks.send_file_to_dropbox}
