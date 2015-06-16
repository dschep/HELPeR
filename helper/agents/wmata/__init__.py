from . import tasks

USER_CONFIG_KEYS = ['api_key']
ACTION_CONFIG_KEYS = {}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = []
CAUSE_TASKS = ['rail_incident']
EFFECT_TASKS = []
