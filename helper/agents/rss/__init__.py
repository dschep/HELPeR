from . import tasks

USER_CONFIG_KEYS = []
ACTION_CONFIG_KEYS = {'secret': 'SecretGenerator'}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CAUSE_TASKS = ['get_rss_feed']
EFFECT_TASKS = ['generate_rss_feed']
