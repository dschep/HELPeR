import base64
from email.mime.text import MIMEText

from celery import shared_task
import requests

from helper.utils.decorators import format_options_from_event


@shared_task
@format_options_from_event
def send_email(data, access_token, from_, to, subject, body, task_pair_id,
               **kwargs):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = from_
    message['subject'] = subject

    resp = requests.post(
        'https://www.googleapis.com/gmail/v1/users/me/messages/send',
        json={'raw': base64.b64encode(bytes(message.as_string(),
                                            'utf-8')).decode('ascii')},
        params={'access_token': access_token},
    )
    resp.raise_for_status()
send_email.options = ['to', 'subject', 'body']
