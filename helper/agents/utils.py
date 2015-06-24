import json

from ..models import Event


def get_from_event_store(task_pair_id, task_type):
    return [{k: json.loads(v) for k, v in event.items()}
            for event in Event.objects.filter(
                task_pair__id=task_pair_id, task_type=task_type)\
            .values_list('data', flat=True)]

def send_to_event_store(data, task_pair_id, task_type):
    Event.objects.create(data={k: json.dumps(v) for k, v in data.items()},
                            task_pair_id=task_pair_id, task_type=task_type)
