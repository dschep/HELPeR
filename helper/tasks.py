from celery import shared_task

from . import models


@shared_task
def run_task_pair(task_pair_id):
    models.TaskPair.objects.get(pk=task_pair_id).run()
