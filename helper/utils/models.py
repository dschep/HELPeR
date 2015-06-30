from helper.models import AgentMeta

from django import forms


class OAuthAgentMixinMeta(AgentMeta):
    def __init__(cls, name, bases, dct):
        if bases: # not 1st base class(the mixin), only subclasses
            from helper.utils.views import OAuth2Login

            class Login(OAuth2Login):
                authorization_url = cls.oauth_opts['authorization_url']
                token_url = cls.oauth_opts['token_url']
                scopes = cls.oauth_opts.get('scopes', [])

            cls.user_config_options = cls.user_config_options.copy()
            cls.user_config_options['app_id'] = forms.CharField()
            cls.user_config_options['app_secret'] = forms.CharField()

            cls.action_config_options = cls.action_config_options.copy()
            cls.action_config_options['access_token'] = Login

        super(OAuthAgentMixinMeta, cls).__init__(name, bases, dct)


class OAuthAgentMixin(metaclass=OAuthAgentMixinMeta):
    pass


class TaskViewAgentMixinMeta(AgentMeta):
    def __init__(cls, name, bases, dct):
        if bases: # not 1st base class(the mixin), only subclasses
            from helper.utils.views import SecretGenerator

            cls.action_config_options = cls.action_config_options.copy()
            cls.action_config_options['secret'] = SecretGenerator

        super(TaskViewAgentMixinMeta, cls).__init__(name, bases, dct)


class TaskViewAgentMixin(metaclass=TaskViewAgentMixinMeta):
    pass
