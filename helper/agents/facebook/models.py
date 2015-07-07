from helper.models import Agent
from helper.utils.models import OAuthAgentMixin
from . import tasks


class FacebookAgent(Agent, OAuthAgentMixin):
    """
    <p>
    Register as a facebook developer at
    <a target="_blank" href="http://developers.facebook.com/">https://developers.facebook.com</a>.
    </p>
    <p>
    Then create an app at <a target="_blank"
    href="https://developers.facebook.com/quickstarts/?platform=web">https://developers.facebook.com/quickstarts/?platform=web</a>
    </p>
    <p>
    Add website as a platorm with
    <kbd>{{ request.scheme }}://{{ request.get_host }}/</kbd>
    as the website and add <kbd>{{ request.get_host }}</kbd> (don't include
    port numbers) as an App Domain.
    </p>
    <p>
    Then enter the <kbd>App id</kbd> and <kbd>App secret</kbd> bellow. Then click
    the Refresh button next to <kbd>Access token</kbd> to connect to your Facebook
    account.
    </p>
    """
    cause_tasks = {
        'check_uploaded_photos': tasks.check_uploaded_photos,
        'check_tagged_photos': tasks.check_tagged_photos,
    }
    oauth_opts = {
        'authorization_url': 'https://www.facebook.com/dialog/oauth',
        'token_url':
            'https://graph.facebook.com/v2.3/oauth/access_token',
        'scopes': ['user_photos'],
    }
    ui = {
        'background': '#4862a3',
        'foreground': 'white',
        'icon': '<i class="fa fa-facebook"></i>'
    }
