from helper.models import Agent
from helper.utils.models import TaskViewAgentMixin
from . import tasks


class RssAgent(Agent, TaskViewAgentMixin):
    """
    <p>
    <kbd>secret</kbd>: click refresh to generate a secret to be used in the RSS
    Agent's feeds' URLs
    </p>
    """
    cause_tasks = {'get_rss_feed': tasks.get_rss_feed}
    effect_tasks = {'generate_rss_feed': tasks.generate_rss_feed}
    ui = {
        'background': '#fe9900',
        'foreground': 'white',
        'icon': '<i class="fa fa-rss"></i>'
    }
