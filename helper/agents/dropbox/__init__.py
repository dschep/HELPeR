from . import tasks

USER_CONFIG_KEYS = ['access_token']
ACTION_CONFIG_KEYS = {}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CAUSE_TASKS = []
EFFECT_TASKS = ['send_file_to_dropbox']
