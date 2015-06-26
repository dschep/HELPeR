from django.core.management.base import BaseCommand, CommandError
from helper.models import Event

class Command(BaseCommand):
    help = 'Delete all Events for a particular task'

    def add_arguments(self, parser):
        parser.add_argument('task_pair_id', nargs='+', type=int)
        parser.add_argument('--no-op', action='store_true', help="dry run")

    def handle(self, *args, **options):
        for task_pair_id in options['task_pair_id']:
            qs = Event.objects.filter(task_pair_id=task_pair_id)
            count = qs.count()
            if not options['no_op']:
                qs.delete()
            self.stdout.write('Deleted {} Events for {}'.format(
                count, task_pair_id))
