from django import forms

from helper.models import Agent
from . import tasks


class GithubAgent(Agent):
    """
    <p>
    Create a Twitter app at <a target="_blank"
    href="https://apps.twitter.com/app/new">https://apps.twitter.com/app/new</a>
    </p>
    <p>
    Go to the 'Keys and Access Tokens' tab and create your access token in the
    'Your Access Token' section.
    </p>
    <p>
    Then enter the <kbd>Consumer Key</kbd>, <kbd>Consumer secret</kbd>
    <kbd>Access token</kbd>, and <kbd>Access token secret</kbd>.
    </p>
    """
    user_config_options = {
        'consumer_key': forms.CharField(),
        'consumer_secret': forms.CharField(),
        'access_token': forms.CharField(),
        'access_token_secret': forms.CharField(),
    }
    cause_tasks = {'sent_tweet': tasks.sent_tweet}
    effect_tasks = {'send_tweet': tasks.send_tweet}
    ui = {
        'background': '#005787',
        'foreground': 'white',
        'icon': '<i class="fa fa-twitter"></i>'
    }
