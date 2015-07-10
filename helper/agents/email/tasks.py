from collections import OrderedDict

from django import forms
from django.conf import settings
from django.core.mail import send_mail as dj_send_email
from celery import shared_task

from helper.utils.decorators import format_options_from_event


@shared_task
@format_options_from_event
def send_email(data, to, subject, body, task_pair_id):
    dj_send_email(subject, body, settings.DEFAULT_FROM_EMAIL,
              [to], fail_silently=False)
send_email.options = OrderedDict([
    ('to', forms.CharField(label='To')),
    ('subject', forms.CharField(label='Subject')),
    ('body', forms.CharField(label='Body', widget=forms.Textarea())),
])
