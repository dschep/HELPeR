from django import forms

from helper.models import Agent
from helper.utils.models import OAuthAgentMixin
from . import tasks


class GmailAgent(Agent, OAuthAgentMixin):
    """
    <p>
    Create a Gmail at <a target="_blank"
    href="https://console.developers.google.com/start/api?id=gmail">https://console.developers.google.com/start/api?id=gmail</a>
    </p>
    <p>
    Create an OAuth Client ID and
    <kbd>{{ request.scheme }}://{{ request.get_host }}/</kbd>
    as the website and add <kbd>{{ request.scheme }}://{{ request.get_host }}{% url 'dispatch_agent_config_url' agent_config_id=object.pk view_name='access_token' %}</kbd>
    as an Redirect URI.
    </p>
    <p>
    Then enter the <kbd>App id</kbd> (client id) and <kbd>App secret</kbd> (client
    secret) bellow.
    </p><p>
    Then click the Refresh button next to <kbd>Access token</kbd>
    to connect to your Gmail account.
    </p>
    <p>
    Enter your email address in <kbd>from</kbd>
    </p>
    """
    user_config_options = {
        'from_': forms.CharField(),
    }
    effect_tasks = {'send_email': tasks.send_email}
    oauth_opts = {
        'authorization_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://www.googleapis.com/oauth2/v3/token',
        'scopes': ['https://www.googleapis.com/auth/gmail.compose'],
    }
