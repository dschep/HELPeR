from functools import wraps

from .dedup.decorators import dedup


def format_options_from_event(func):
    """
    MUST(ok.. should) be the first decorator used since it actually wraps the
    function and all others just add stuff (at least HELPeR decorators)

    Applies formatting to all keys if task_pair_id isn't present, else looks up
    the effect task's options and only formats those.
    """
    @wraps(func)
    def wrapper(data, **kwargs):
        from helper.models import TaskPair  # Avoid circular import
        try:
            options = TaskPair.objects.get(
                pk=kwargs['task_pair_id']).effect.options
        except (TaskPair.DoesNotExist, KeyError):
            options = kwargs.keys()
        for option in options:
            kwargs[option] = kwargs[option].format(**data)
        return func(data, **kwargs)
    return wrapper
