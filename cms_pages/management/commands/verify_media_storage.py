import uuid
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Verifies that production media storage is durable Bucketeer/S3 and publicly readable."

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=20)

    def handle(self, *args, **options):
        timeout = options["timeout"]

        if isinstance(default_storage, FileSystemStorage):
            raise CommandError(
                "Production media storage is FileSystemStorage. Bucketeer/S3 is required."
            )

        storage_class = default_storage.__class__
        storage_module = storage_class.__module__
        if "storages.backends.s3" not in storage_module:
            raise CommandError(
                f"Unexpected production media storage: {storage_module}.{storage_class.__name__}"
            )

        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
        region = getattr(settings, "AWS_S3_REGION_NAME", "")
        if not bucket or not region:
            raise CommandError("Bucketeer bucket/region settings are missing.")

        marker_name = f"healthchecks/chatgpt-media-{uuid.uuid4().hex}.txt"
        saved_name = None

        try:
            saved_name = default_storage.save(
                marker_name,
                ContentFile(b"salymbekov-media-storage-ok\n"),
            )

            if not default_storage.exists(saved_name):
                raise CommandError("S3 upload completed but the object cannot be found.")

            with default_storage.open(saved_name, "rb") as stored_file:
                payload = stored_file.read()
            if payload != b"salymbekov-media-storage-ok\n":
                raise CommandError("S3 read-back returned unexpected content.")

            public_url = default_storage.url(saved_name)
            if "/public/" not in public_url:
                raise CommandError(
                    f"Media URL is not under Bucketeer's public/ prefix: {public_url}"
                )

            request = Request(
                public_url,
                headers={"User-Agent": "SalymbekovStorageHealthcheck/1.0"},
            )
            with urlopen(request, timeout=timeout) as response:
                public_payload = response.read()
                status = getattr(response, "status", 200)

            if status >= 400 or public_payload != payload:
                raise CommandError(
                    f"S3 object is not publicly readable (HTTP {status})."
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Bucketeer/S3 OK: bucket={bucket}, region={region}, public media URL verified."
                )
            )
        except CommandError:
            raise
        except Exception as exc:
            raise CommandError(f"Bucketeer/S3 verification failed: {exc}") from exc
        finally:
            if saved_name:
                try:
                    default_storage.delete(saved_name)
                except Exception as cleanup_exc:
                    self.stderr.write(
                        self.style.WARNING(
                            f"Could not delete storage healthcheck object {saved_name}: {cleanup_exc}"
                        )
                    )
