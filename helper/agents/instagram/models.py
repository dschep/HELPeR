from helper.models import Agent
from helper.utils.models import OAuthAgentMixin
from . import tasks


class InstagramAgent(Agent, OAuthAgentMixin):
    """
    <p>
    Create an app at <a target="_blank"
    href="https://instagram.com/developer/clients/manage/">https://instagram.com/developer/clients/manage/</a>
    </p>
    <p>
    Add website as a platorm with
    <kbd>{{ request.scheme }}://{{ request.get_host }}/</kbd>
    as the website and add <kbd>{{ request.scheme }}://{{ request.get_host }}{% url 'dispatch_agent_config_url' agent_config_id=object.pk view_name='access_token' %}</kbd>
    as an Redirect URI.
    </p>
    <p>
    Then enter the <kbd>App id</kbd>(client id) and <kbd>App secret</kbd>(client
    secret) bellow. Then click the Refresh button next to <kbd>Access token</kbd>
    to connect to your Instagram account.
    </p>
    """
    cause_tasks = {
        'check_uploaded_photos': tasks.check_uploaded_photos,
        'check_liked_photos': tasks.check_liked_photos,
    }
    oauth_opts = {
        'authorization_url': 'https://api.instagram.com/oauth/authorize/',
        'token_url': 'https://api.instagram.com/oauth/access_token'
    }
