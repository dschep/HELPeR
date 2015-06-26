from . import tasks

USER_CONFIG_KEYS = ['user', 'access_token']
ACTION_CONFIG_KEYS = {}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CAUSE_TASKS = ['get_notifications']
EFFECT_TASKS = []
