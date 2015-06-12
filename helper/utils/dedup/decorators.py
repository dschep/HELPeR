def dedup(key):
    def decorator(task):
        task.dedup_key = key
        return task
    return decorator
