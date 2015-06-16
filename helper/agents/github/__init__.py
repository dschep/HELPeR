from . import tasks

USER_CONFIG_KEYS = ['access_token']
ACTION_CONFIG_KEYS = {}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = []
CAUSE_TASKS = ['get_notifications']
EFFECT_TASKS = []
