import json
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Max
from django.utils.text import slugify

from cms_pages.models import Page, PageDocument, PageMedia


WORDPRESS_ASSET_RE = re.compile(
    r"https?://(?:www\.)?salymbekov\.com/wp-content/uploads/[^\s\"'<>]+",
    re.IGNORECASE,
)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif", ".bmp"}


def clean_asset_url(value):
    return (value or "").rstrip(".,;:)]}")


def collect_urls(value):
    if not value:
        return set()
    return {clean_asset_url(match) for match in WORDPRESS_ASSET_RE.findall(str(value))}


def safe_filename(url):
    parsed = urlparse(url)
    original = Path(parsed.path).name or "asset"
    suffix = Path(original).suffix.lower()
    stem = slugify(Path(original).stem) or "asset"
    return f"{stem}{suffix}" if suffix else stem


class Command(BaseCommand):
    help = (
        "Finds old salymbekov.com WordPress uploads used by CMS pages and sections. "
        "With --apply downloads them into Django storage (S3/Bucketeer in production) "
        "and rewrites CMS HTML/JSON/links to the new storage URLs."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist migration. Without this flag the command only audits remaining external assets.",
        )
        parser.add_argument(
            "--only-path",
            action="append",
            default=[],
            help="Limit the audit/migration to one or more CMS page paths.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=45,
            help="Download timeout per file in seconds (default: 45).",
        )

    def handle(self, *args, **options):
        self.apply = options["apply"]
        self.timeout = options["timeout"]
        only_paths = set(options["only_path"] or [])

        queryset = Page.objects.all().prefetch_related("sections", "media_items", "documents", "links")
        if only_paths:
            queryset = queryset.filter(path__in=only_paths)

        pages_with_refs = 0
        references_found = 0
        migrated = 0
        failed = 0
        unresolved = []

        for page in queryset:
            refs = self._collect_page_refs(page)
            if not refs:
                continue

            pages_with_refs += 1
            references_found += len(refs)
            self.stdout.write(f"{page.path}: {len(refs)} external WordPress asset(s)")

            if not self.apply:
                for url in sorted(refs):
                    self.stdout.write(f"  - {url}")
                continue

            replacements = {}
            for url in sorted(refs):
                try:
                    new_url = self._migrate_asset(page, url)
                except Exception as exc:
                    failed += 1
                    unresolved.append((page.path, url, str(exc)))
                    self.stderr.write(self.style.WARNING(f"  failed: {url}: {exc}"))
                    continue

                if new_url and new_url != url:
                    replacements[url] = new_url
                    migrated += 1
                    self.stdout.write(self.style.SUCCESS(f"  migrated: {url} -> {new_url}"))
                else:
                    failed += 1
                    unresolved.append((page.path, url, "no replacement URL"))

            if replacements:
                self._rewrite_page(page, replacements)

        mode = "MIGRATION" if self.apply else "AUDIT"
        self.stdout.write(
            self.style.SUCCESS(
                f"{mode} complete: pages={pages_with_refs}, refs={references_found}, "
                f"migrated={migrated}, failed={failed}."
            )
        )

        if unresolved:
            self.stderr.write("Unresolved external assets:")
            for path, url, reason in unresolved:
                self.stderr.write(f"  {path} | {url} | {reason}")

    def _collect_page_refs(self, page):
        refs = set()

        for field_name in ("body_ru", "body_en", "body_kg"):
            refs.update(collect_urls(getattr(page, field_name, "")))

        for section in page.sections.all():
            for field_name in ("body_ru", "body_en", "body_kg"):
                refs.update(collect_urls(getattr(section, field_name, "")))

        try:
            refs.update(collect_urls(json.dumps(page.data or {}, ensure_ascii=False)))
        except (TypeError, ValueError):
            pass

        for media in page.media_items.all():
            refs.update(collect_urls(media.external_url))

        for document in page.documents.all():
            refs.update(collect_urls(document.external_url))

        for link in page.links.all():
            refs.update(collect_urls(link.url))

        return refs

    def _download(self, url):
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; SalymbekovMediaMigrator/1.0)",
                "Accept": "*/*",
            },
        )
        with urlopen(request, timeout=self.timeout) as response:
            return response.read()

    def _migrate_asset(self, page, url):
        existing_media = page.media_items.filter(external_url=url).first()
        existing_document = page.documents.filter(external_url=url).first()

        if existing_media and existing_media.file:
            existing_media.external_url = ""
            existing_media.save(update_fields=["external_url", "updated_at"])
            return existing_media.resolved_url

        if existing_document and existing_document.file:
            existing_document.external_url = ""
            existing_document.save(update_fields=["external_url", "updated_at"])
            return existing_document.resolved_url

        content = self._download(url)
        filename = safe_filename(url)
        suffix = Path(urlparse(url).path).suffix.lower()

        if existing_media:
            target = existing_media
            target.file.save(filename, ContentFile(content), save=False)
            target.external_url = ""
            target.save()
            return target.resolved_url

        if existing_document:
            target = existing_document
            target.file.save(filename, ContentFile(content), save=False)
            target.external_url = ""
            target.save()
            return target.resolved_url

        if suffix in IMAGE_EXTENSIONS:
            next_order = (page.media_items.aggregate(max_order=Max("order"))["max_order"] or 0) + 1
            target = PageMedia(page=page, media_type=PageMedia.TYPE_IMAGE, order=next_order)
            target.file.save(filename, ContentFile(content), save=False)
            target.save()
            return target.resolved_url

        next_order = (page.documents.aggregate(max_order=Max("order"))["max_order"] or 0) + 1
        target = PageDocument(page=page, order=next_order)
        target.file.save(filename, ContentFile(content), save=False)
        target.save()
        return target.resolved_url

    @staticmethod
    def _replace_urls(value, replacements):
        updated = value or ""
        for old_url, new_url in replacements.items():
            updated = updated.replace(old_url, new_url)
        return updated

    def _rewrite_page(self, page, replacements):
        update_fields = []

        for field_name in ("body_ru", "body_en", "body_kg"):
            value = getattr(page, field_name, "") or ""
            updated = self._replace_urls(value, replacements)
            if updated != value:
                setattr(page, field_name, updated)
                update_fields.append(field_name)

        try:
            serialized = json.dumps(page.data or {}, ensure_ascii=False)
            updated_serialized = self._replace_urls(serialized, replacements)
            if updated_serialized != serialized:
                page.data = json.loads(updated_serialized)
                update_fields.append("data")
        except (TypeError, ValueError):
            self.stderr.write(self.style.WARNING(f"  could not rewrite JSON data for {page.path}"))

        if update_fields:
            page.save(update_fields=[*update_fields, "updated_at"])

        for section in page.sections.all():
            section_update_fields = []
            for field_name in ("body_ru", "body_en", "body_kg"):
                value = getattr(section, field_name, "") or ""
                updated = self._replace_urls(value, replacements)
                if updated != value:
                    setattr(section, field_name, updated)
                    section_update_fields.append(field_name)
            if section_update_fields:
                section.save(update_fields=[*section_update_fields, "updated_at"])

        for link in page.links.all():
            new_url = replacements.get(link.url)
            if new_url:
                link.url = new_url
                link.save(update_fields=["url", "updated_at"])
