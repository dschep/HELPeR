from datetime import datetime, timedelta

from helper.utils.views import OAuth2Login


class FBLogin(OAuth2Login):
    authorization_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
    extra_save = {'expires_in': lambda x: (timedelta(seconds=x) +
                                           datetime.now()).isoformat()}
    scopes = ['user_photos']
