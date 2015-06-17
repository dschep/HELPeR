from django.core.management.base import BaseCommand, CommandError
from helper.models import TaskPair

class Command(BaseCommand):
    help = 'Popoulate DedupEvents for a particular task'

    def add_arguments(self, parser):
        parser.add_argument('task_pair_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for task_pair_id in options['task_pair_id']:
            TaskPair.objects.get(pk=task_pair_id).populate_dedup_events()
            self.stdout.write('Populating DedupEvents for {}'.format(
                task_pair_id))
