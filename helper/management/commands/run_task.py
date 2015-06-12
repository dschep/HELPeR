from django.core.management.base import BaseCommand, CommandError
from helper.models import TaskPair

class Command(BaseCommand):
    help = 'Runs the specified task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs='+', type=int)
        parser.add_argument('--wait', action='store_true')

    def handle(self, *args, **options):
        for task_id in options['task_id']:
            try:
                task = TaskPair.objects.get(pk=task_id)
            except TaskPair.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)

            res = task.run()
            if options['wait']:
                res.get()
                if res.successful():
                    msg = 'Successfully ran'
                else:
                    msg = 'Error while running'
            else:
                msg = 'Launched'

            self.stdout.write('{} task {}'.format(msg, task))
