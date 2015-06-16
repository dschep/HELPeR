import posixpath

import requests
from celery import shared_task
from dropbox.client import DropboxClient


@shared_task
def send_file_to_dropbox(data, task_pair_id, access_token,
                                       filename, path, url):
    client = DropboxClient(access_token)
    file_path = posixpath.join(path.format(**data),
                                filename.format(**data))
    file_path = file_path.replace('\\', '|')
    file_path = file_path.encode('ascii', errors='replace').decode()
    resp = requests.get(data[url.format(**data)])
    resp.raise_for_status()
    response = client.put_file(file_path, resp.content)

send_file_to_dropbox.options = ['filename', 'path', 'url']
