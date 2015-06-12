from helper.utils.views import OAuth2Login


class InstagramLogin(OAuth2Login):
    authorization_url = 'https://api.instagram.com/oauth/authorize/'
    token_url = 'https://api.instagram.com/oauth/access_token'
