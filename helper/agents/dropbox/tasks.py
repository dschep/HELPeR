import posixpath

import requests
from celery import shared_task
from dropbox.client import DropboxClient


@shared_task
def send_send_file_from_url_to_dropbox(data, task_pair_id, access_token,
                                       name_fmt, path='/HELPeR/',
                                       url_key='url'):
    client = DropboxClient(access_token)
    file_path = posixpath.join(path.format(**data),
                                name_fmt.format(**data))
    file_path = file_path.replace('\\', '|')
    file_path = file_path.encode('ascii', errors='replace').decode()
    resp = requests.get(data[url_key])
    resp.raise_for_status()
    response = client.put_file(file_path, resp.content)
    pass
