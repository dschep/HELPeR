from . import tasks, views

USER_CONFIG_KEYS = ['app_id', 'app_secret', 'from_']
ACTION_CONFIG_KEYS = {
    'access_token': 'GmailLogin'
}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = ['GmailLogin']
CAUSE_TASKS = []
EFFECT_TASKS = ['send_email']
