from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
import requests


class OAuth2Login(View):
    authorization_url = None
    token_url = None
    extra_save = None
    scopes = []

    def get(self, request, agent_config):
        if 'code' in request.GET:
            params = {
                'client_id': agent_config.options['app_id'],
                'client_secret': agent_config.options['app_secret'],
                'code': request.GET['code'],
                'redirect_uri': request.build_absolute_uri().split('?')[0],
                'grant_type': 'authorization_code',
            }
            resp = requests.post(self.token_url, data=params)
            resp.raise_for_status()

            agent_config.options['access_token'] = resp.json()['access_token']
            if self.extra_save:
                for key, func in self.extra_save.items():
                    agent_config.options[key] = func(resp.json()[key])
            agent_config.save()

            return redirect(reverse('agent_config_detail', kwargs={
                'pk': agent_config.pk}))
        else:
            return redirect(self.authorization_url +
                            ('?client_id={app_id}&response_type=code'
                             '&redirect_uri={redirect_uri}&scope={scope}').format(
                                 app_id=agent_config.options['app_id'],
                                 redirect_uri=request.build_absolute_uri(),
                                 scope=','.join(self.scopes),
                             ))
