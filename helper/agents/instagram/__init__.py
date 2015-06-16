from . import tasks, views

USER_CONFIG_KEYS = ['app_id', 'app_secret']
ACTION_CONFIG_KEYS = {
    'access_token': 'InstagramLogin'
}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = ['InstagramLogin']
CAUSE_TASKS = ['check_uploaded_photos']
EFFECT_TASKS = []
