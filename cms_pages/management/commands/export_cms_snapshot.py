import os
from django.core.management.base import BaseCommand, CommandError
from cms_pages.models import ContentSnapshot


class Command(BaseCommand):
    help = 'Export a private CMS snapshot to a new owner-only local file for recovery with loaddata.'

    def add_arguments(self, parser):
        parser.add_argument('snapshot_id', type=int)
        parser.add_argument('--output', required=True)

    def handle(self, *args, **options):
        try:
            snapshot = ContentSnapshot.objects.get(pk=options['snapshot_id'])
            descriptor = os.open(options['output'], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, 'w') as stream:
                stream.write(snapshot.payload)
        except (ContentSnapshot.DoesNotExist, OSError) as exc:
            raise CommandError('Snapshot not found or unable to create a new output file.') from exc
        self.stdout.write(f'Exported snapshot {snapshot.pk}.')
