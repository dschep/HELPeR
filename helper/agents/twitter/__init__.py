from . import tasks, views

USER_CONFIG_KEYS = ['consumer_key', 'consumer_secret',
                    'access_token', 'access_token_secret']
ACTION_CONFIG_KEYS = {}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = []
CAUSE_TASKS = ['sent_tweet']
EFFECT_TASKS = ['send_tweet']
