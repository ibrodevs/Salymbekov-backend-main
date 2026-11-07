import os
import hashlib
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cms_pages.models import ContentSnapshot
from cms_pages.university_update import apply_update, content_models


class Command(BaseCommand):
    help = 'Preview by default; --apply requires a file or durable database backup.'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true')
        parser.add_argument('--backup')
        parser.add_argument('--database-backup', action='store_true', help='Persist a private CMS snapshot in PostgreSQL before applying.')

    def handle(self, *args, **options):
        if options['apply']:
            if not options['backup'] and not options['database_backup']:
                raise CommandError('--backup or --database-backup is required before modifying content')
            # Exclusive creation prevents overwriting a previous snapshot; owner-only permissions.
            try:
                if not options['backup']:
                    fd = None
                else:
                    fd = os.open(options['backup'], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                if fd is not None:
                    with os.fdopen(fd, 'w') as stream:
                        serializers.serialize('json', (obj for model in content_models() for obj in model.objects.all().order_by('pk')), stream=stream)
            except OSError as exc:
                raise CommandError('Unable to create a new backup file') from exc
        with transaction.atomic():
            if options['apply'] and options['database_backup']:
                payload = serializers.serialize('json', (obj for model in content_models() for obj in model.objects.all().order_by('pk')))
                digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
                snapshot, _ = ContentSnapshot.objects.get_or_create(digest=digest, defaults={'payload': payload})
                self.stdout.write(f'Private database CMS snapshot: {snapshot.pk}')
            counts = apply_update()
            for name, count in counts.items():
                self.stdout.write(f'{name}: {count}')
            if not options['apply']:
                transaction.set_rollback(True)
        self.stdout.write('Applied; backup saved.' if options['apply'] else 'Preview only; no changes saved.')
