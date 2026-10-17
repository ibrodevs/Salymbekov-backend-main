from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Command(BaseCommand):
    help = (
        "Copies every existing Django FileField/ImageField object from the legacy "
        "Bucketeer bucket root into the production public/ prefix. Database file "
        "names stay unchanged, so the new default storage resolves them correctly."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail if any database-referenced file cannot be found in S3 or local media.",
        )

    def handle(self, *args, **options):
        strict = options["strict"]

        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
        region = getattr(settings, "AWS_S3_REGION_NAME", "")
        access_key = getattr(settings, "AWS_ACCESS_KEY_ID", "")
        secret_key = getattr(settings, "AWS_SECRET_ACCESS_KEY", "")
        destination_location = getattr(default_storage, "location", "") or ""

        if not all([bucket, region, access_key, secret_key]):
            raise CommandError("Bucketeer/S3 credentials are required for existing-file migration.")
        if destination_location.strip("/") != "public":
            raise CommandError(
                f"Destination storage must use location='public', got {destination_location!r}."
            )

        legacy_storage = S3Boto3Storage(
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket,
            region_name=region,
            location="",
            default_acl=None,
            file_overwrite=False,
            querystring_auth=False,
        )

        logical_names = self._collect_file_names()
        copied = 0
        already_present = 0
        recovered_local = 0
        missing = []

        self.stdout.write(f"Existing Django file references found: {len(logical_names)}")

        for name in sorted(logical_names):
            normalized_name = str(name).lstrip("/")
            if not normalized_name:
                continue

            # FileField stores the logical object name, not the storage location.
            # Under the new storage this name resolves to public/<name>.
            if default_storage.exists(normalized_name):
                already_present += 1
                continue

            if legacy_storage.exists(normalized_name):
                try:
                    with legacy_storage.open(normalized_name, "rb") as source:
                        saved_name = default_storage.save(normalized_name, File(source))
                    if saved_name != normalized_name:
                        raise CommandError(
                            f"Unexpected renamed destination for {normalized_name}: {saved_name}"
                        )
                    copied += 1
                    self.stdout.write(self.style.SUCCESS(f"  copied: {normalized_name}"))
                    continue
                except Exception as exc:
                    missing.append((normalized_name, f"S3 copy failed: {exc}"))
                    self.stderr.write(self.style.WARNING(f"  failed: {normalized_name}: {exc}"))
                    continue

            # Recovery path for a file that was committed/bundled locally rather than
            # uploaded to the legacy bucket. This is intentionally only a fallback.
            media_root = getattr(settings, "BASE_DIR", Path.cwd()) / "media"
            local_path = media_root / normalized_name
            if local_path.is_file():
                try:
                    with local_path.open("rb") as source:
                        saved_name = default_storage.save(normalized_name, File(source))
                    if saved_name != normalized_name:
                        raise CommandError(
                            f"Unexpected renamed destination for {normalized_name}: {saved_name}"
                        )
                    recovered_local += 1
                    self.stdout.write(self.style.SUCCESS(f"  recovered local: {normalized_name}"))
                    continue
                except Exception as exc:
                    missing.append((normalized_name, f"local recovery failed: {exc}"))
                    self.stderr.write(self.style.WARNING(f"  failed local recovery: {normalized_name}: {exc}"))
                    continue

            missing.append((normalized_name, "not found in legacy S3 root or local media"))
            self.stderr.write(self.style.WARNING(f"  missing source: {normalized_name}"))

        self.stdout.write(
            self.style.SUCCESS(
                "Existing S3 file migration complete: "
                f"referenced={len(logical_names)}, copied={copied}, "
                f"already_public={already_present}, recovered_local={recovered_local}, "
                f"missing={len(missing)}."
            )
        )

        if strict and missing:
            details = "\n".join(f"  {name}: {reason}" for name, reason in missing[:50])
            if len(missing) > 50:
                details += f"\n  ... and {len(missing) - 50} more"
            raise CommandError(
                "Some database-referenced files could not be migrated into public/ Bucketeer storage:\n"
                + details
            )

    @staticmethod
    def _collect_file_names():
        names = set()

        for model in apps.get_models():
            file_fields = [
                field
                for field in model._meta.get_fields()
                if isinstance(field, models.FileField) and not field.auto_created
            ]
            if not file_fields:
                continue

            manager = model._default_manager
            for field in file_fields:
                try:
                    values = (
                        manager.exclude(**{f"{field.name}__isnull": True})
                        .exclude(**{field.name: ""})
                        .values_list(field.name, flat=True)
                        .distinct()
                    )
                    for value in values.iterator():
                        if value:
                            names.add(str(value))
                except Exception:
                    # Some third-party/unmanaged models can expose FileField-like
                    # metadata without a queryable table. They are not site uploads.
                    continue

        return names
