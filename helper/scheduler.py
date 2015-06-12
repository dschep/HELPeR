from datetime import timedelta

from celery.beat import PersistentScheduler
from celery import __version__
from celery.five import items, values
from celery.utils.log import get_logger

from . import models


logger = get_logger(__name__)
debug, info, error, warning = (logger.debug, logger.info,
                               logger.error, logger.warning)


class TaskPairScheduler(PersistentScheduler):
    def _get_taskpair_tasks(self):
        tasks = {}
        for task_pair in models.TaskPair.objects.all():
            if hasattr(task_pair.cause, 'every'):
                every = task_pair.cause.every
            elif '_every' in task_pair.cause_options:
                every = int(task_pair.cause_options['_every'])
            else:
                continue

            tasks['run-task-pair-{}'.format(task_pair.id)] = {
                'task': 'helper.tasks.run_task_pair',
                'schedule': timedelta(minutes=every),
                'args': (task_pair.id,),
            }
        return tasks

    def get_schedule(self):
        self.merge_inplace(self._get_taskpair_tasks())
        self.install_default_entries(self._store['entries'])
        return self._store['entries']

    def set_schedule(self, schedule):
        self._store['entries'] = schedule
    schedule = property(get_schedule, set_schedule)

    def merge_inplace(self, b):
        """ PersistentScheduler + s/self.scheduler/self._store['entries'] """
        schedule = self._store['entries']
        A, B = set(schedule), set(b)

        # Remove items from disk not in the schedule anymore.
        for key in A ^ B:
            schedule.pop(key, None)

        # Update and add new items in the schedule
        for key in B:
            entry = self.Entry(**dict(b[key], name=key, app=self.app))
            if schedule.get(key):
                schedule[key].update(entry)
            else:
                schedule[key] = entry

    def setup_schedule(self):
        """ PersistentScheduler + s/self.scheduler/self._store['entries'] """
        try:
            self._store = self.persistence.open(self.schedule_filename,
                                                writeback=True)
        except Exception as exc:
            error('Removing corrupted schedule file %r: %r',
                  self.schedule_filename, exc, exc_info=True)
            self._remove_db()
            self._store = self.persistence.open(self.schedule_filename,
                                                writeback=True)
        else:
            try:
                self._store['entries']
            except KeyError:
                # new schedule db
                self._store['entries'] = {}
            else:
                if '__version__' not in self._store:
                    warning('DB Reset: Account for new __version__ field')
                    self._store.clear()   # remove schedule at 2.2.2 upgrade.
                elif 'tz' not in self._store:
                    warning('DB Reset: Account for new tz field')
                    self._store.clear()   # remove schedule at 3.0.8 upgrade
                elif 'utc_enabled' not in self._store:
                    warning('DB Reset: Account for new utc_enabled field')
                    self._store.clear()   # remove schedule at 3.0.9 upgrade

        tz = self.app.conf.CELERY_TIMEZONE
        stored_tz = self._store.get('tz')
        if stored_tz is not None and stored_tz != tz:
            warning('Reset: Timezone changed from %r to %r', stored_tz, tz)
            self._store.clear()   # Timezone changed, reset db!
        utc = self.app.conf.CELERY_ENABLE_UTC
        stored_utc = self._store.get('utc_enabled')
        if stored_utc is not None and stored_utc != utc:
            choices = {True: 'enabled', False: 'disabled'}
            warning('Reset: UTC changed from %s to %s',
                    choices[stored_utc], choices[utc])
            self._store.clear()   # UTC setting changed, reset db!
        entries = self._store.setdefault('entries', {})
        self.merge_inplace(self.app.conf.CELERYBEAT_SCHEDULE)
        self.install_default_entries(self._store['entries'])
        self._store.update(__version__=__version__, tz=tz, utc_enabled=utc)
        self.sync()
        debug('Current schedule:\n' + '\n'.join(
            repr(entry) for entry in values(entries)))

    def update_from_dict(self, dict_):
        """ PersistentScheduler + s/self.scheduler/self._store['entries'] """
        self._store['entries'].update({
            name: self._maybe_entry(name, entry)
            for name, entry in items(dict_)
        })


def schedule(every):
    def decorator(task):
        task.every = every
        return task
    return decorator
