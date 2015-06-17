import posixpath

import requests
from celery import shared_task
from dropbox.client import DropboxClient

from helper.utils.decorators import format_options_from_event


@shared_task
@format_options_from_event
def send_file_to_dropbox(data, task_pair_id, access_token,
                         filename, path, url):
    client = DropboxClient(access_token)
    file_path = posixpath.join(path, filename)
    file_path = file_path.replace('\\', '|')
    file_path = file_path.encode('ascii', errors='replace').decode()
    resp = requests.get(url)
    resp.raise_for_status()
    client.put_file(file_path, resp.content, overwrite=True)

send_file_to_dropbox.options = ['filename', 'path', 'url']
