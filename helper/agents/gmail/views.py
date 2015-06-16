from helper.utils.views import OAuth2Login


class GmailLogin(OAuth2Login):
    authorization_url = 'https://accounts.google.com/o/oauth2/auth'
    token_url = 'https://www.googleapis.com/oauth2/v3/token'
    scopes = ['https://www.googleapis.com/auth/gmail.compose']
