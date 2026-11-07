import os
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cms_pages.university_update import apply_update, content_models


class Command(BaseCommand):
    help = 'Preview CMS update by default; --apply requires a new backup file.'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true')
        parser.add_argument('--backup')

    def handle(self, *args, **options):
        if options['apply']:
            if not options['backup']:
                raise CommandError('--backup is required before modifying content')
            # Exclusive creation prevents overwriting a previous snapshot; owner-only permissions.
            try:
                fd = os.open(options['backup'], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, 'w') as stream:
                    serializers.serialize('json', (obj for model in content_models() for obj in model.objects.all()), stream=stream)
            except OSError as exc:
                raise CommandError('Unable to create a new backup file') from exc
        with transaction.atomic():
            counts = apply_update()
            for name, count in counts.items():
                self.stdout.write(f'{name}: {count}')
            if not options['apply']:
                transaction.set_rollback(True)
        self.stdout.write('Applied; backup saved.' if options['apply'] else 'Preview only; no changes saved.')
