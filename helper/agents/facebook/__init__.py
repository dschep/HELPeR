from . import tasks, views

USER_CONFIG_KEYS = ['app_id', 'app_secret']
ACTION_CONFIG_KEYS = {
    'access_token': 'FBLogin'
}
CONFIG_KEYS = USER_CONFIG_KEYS + list(ACTION_CONFIG_KEYS.keys())
CONFIG_ACTIONS = ['FBLogin']
