from collections import OrderedDict

import requests
from django import forms
from celery import shared_task

from helper.utils.decorators import format_options_from_event


@shared_task
@format_options_from_event
def http_request(data, method, url, verify,
                 user=None, pass_=None, data_=None, json=None,
                 task_pair_id=None):

    kwargs = {}

    if user or pass_:
        kwargs['auth'] = (user, pass_)
    if json:
        kwargs['json'] = json
    if data_:
        kwargs['data'] = data_
    if verify == 'false':
        kwargs['verify'] = False

    resp = requests.request(method, url, **kwargs)
    resp.raise_for_status()

http_request.options = OrderedDict([
    ('method', forms.ChoiceField(label='Method', choices=[
        ('GET',)*2,
        ('POST',)*2,
        ('PUT',)*2,
        ('PATCH',)*2,
        ('DELETE',)*2,
        ('HEAD',)*2,
    ])),
    ('url', forms.CharField(label='URL')),
    ('user', forms.CharField(label='User', required=False)),
    ('pass_', forms.CharField(label='Password', required=False,
                              widget=forms.PasswordInput())),
    ('data_', forms.CharField(label='Data', required=False,
                             widget=forms.Textarea())),
    ('json', forms.CharField(label='JSON', required=False,
                             widget=forms.Textarea())),
    ('verify', forms.ChoiceField(label='Verify SSL Certs', required=True,
                                 choices=[('true', 'Yes'), ('false', 'No')])),
])


@shared_task
@format_options_from_event
def http_request_urldownload(data, method, url, verify, data_url,
                             user=None, pass_=None,
                             task_pair_id=None):

    resp = requests.get(data_url)
    resp.raise_for_status()

    kwargs = {'data': resp.content}

    if user or pass_:
        kwargs['auth'] = (user, pass_)
    if verify == 'false':
        kwargs['verify'] = False

    resp = requests.request(method, url, **kwargs)
    resp.raise_for_status()

http_request_urldownload.options = OrderedDict([
    ('method', forms.ChoiceField(label='Method', choices=[
        ('GET',)*2,
        ('POST',)*2,
        ('PUT',)*2,
        ('PATCH',)*2,
        ('DELETE',)*2,
        ('HEAD',)*2,
    ])),
    ('url', forms.CharField(label='URL')),
    ('data_url', forms.CharField(label='Data URL',
                                 help_text=('URL to download data for upload'
                                            ' from'))),
    ('user', forms.CharField(label='User', required=False)),
    ('pass_', forms.CharField(label='Password', required=False,
                              widget=forms.PasswordInput())),
    ('verify', forms.ChoiceField(label='Verify SSL Certs', required=True,
                                 choices=[('true', 'Yes'), ('false', 'No')])),
])
