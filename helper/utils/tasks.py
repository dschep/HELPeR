from celery import shared_task, subtask, group

@shared_task
def dmap(iter, callback):
    # Map a callback over an iterator and return as a group
    callback = subtask(callback)
    return group(callback.clone([arg,]) for arg in iter)()
