from celery import shared_task

from helper.celery import app


@shared_task
def create_dedup_event(data, dedup_key, task_pair_id):
    from helper.models import DedupEvent # avoid recursive import.
    return DedupEvent.objects.get_or_create(
        task_pair_id=task_pair_id, key=data[dedup_key])[1]

@shared_task
def dedup_effect_wrapper(data, dedup_key, task_pair_id, effect):
    from helper.models import DedupEvent # avoid recursive import.
    if DedupEvent.objects.get_or_create(task_pair_id=task_pair_id,
                                        key=data[dedup_key])[1]:
        effect.apply_async(
            (data,), link_error=remove_from_dedup_cache_on_error.s(
                dedup_key, task_pair_id, data))
        return data

@shared_task
def remove_from_dedup_cache_on_error(task_id, dedup_key, task_pair_id, data):
    from helper.models import DedupEvent # avoid recursive import.
    DedupEvent.objects.filter(task_pair_id=task_pair_id,
                              key=data[dedup_key]).delete()
