import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cms_pages.models import Page, PageDocument, PageMedia
from presscentre.models import News


PAYLOAD_PATH = Path(__file__).resolve().parents[2] / "legacy_parity" / "payload.json"
CONTENT_STATUS = "legacy-parity"
WORDPRESS_UPLOAD_RE = re.compile(r"https?://(?:www\.)?salymbekov\.com/wp-content/uploads/[^\s\"'<>]+", re.I)
LANGS = ("ru", "en", "kg")


class Command(BaseCommand):
    help = (
        "Makes existing CMS pages match their counterparts on the official site salymbekov.com "
        "(cms_pages/legacy_parity/payload.json, built by tools/build_legacy_parity.py). "
        "Without flags it only prints what would change.\n"
        "Order: --apply, then `migrate_external_media --apply --strict` (moves legacy files to S3), "
        "then --finalize, then --check."
    )

    def add_arguments(self, parser):
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument("--apply", action="store_true", help="Write payload content into CMS pages and news.")
        mode.add_argument(
            "--finalize",
            action="store_true",
            help="After media migration: drop gallery/document records that only duplicate files embedded in the page text.",
        )
        mode.add_argument("--check", action="store_true", help="Verify pages match the payload and no legacy file URLs remain.")
        parser.add_argument("--payload", default=str(PAYLOAD_PATH))

    def handle(self, *args, **options):
        payload_path = Path(options["payload"])
        if not payload_path.exists():
            raise CommandError(f"Payload not found: {payload_path}")
        payload = json.loads(payload_path.read_text(encoding="utf-8"))

        if options["finalize"]:
            return self.finalize(payload)
        if options["check"]:
            return self.verify(payload)
        return self.sync(payload, apply=options["apply"])

    # ------------------------------------------------------------------ sync
    def sync(self, payload, apply):
        pages = payload["pages"]
        missing = [item["path"] for item in pages if not Page.objects.filter(path=item["path"]).exists()]
        if missing:
            self.stdout.write(self.style.WARNING(f"Pages missing in CMS (will be created): {', '.join(missing)}"))

        if not apply:
            for item in pages:
                page = Page.objects.filter(path=item["path"]).first()
                current = (page.title_ru if page else "") or "—"
                self.stdout.write(f"{item['path']}: «{current}» -> «{item['title']['ru']}»")
            self.stdout.write(self.style.WARNING(f"DRY RUN: {len(pages)} pages would be replaced. Run with --apply."))
            return

        with transaction.atomic():
            for item in pages:
                self.apply_page(item, payload)
            news_changed = self.apply_news(payload)

        self.stdout.write(self.style.SUCCESS(f"Applied legacy content to {len(pages)} pages; news updated: {news_changed}."))
        self.stdout.write("Next: python manage.py migrate_external_media --apply --strict")

    def apply_page(self, item, payload):
        page, _ = Page.objects.get_or_create(path=item["path"], defaults={"admin_title": item["title"]["ru"]})

        page.sections.all().delete()
        page.cards.all().delete()
        page.stats.all().delete()
        page.media_items.all().delete()
        page.documents.all().delete()
        page.links.all().delete()

        for lang in LANGS:
            title = item["title"].get(lang) or item["title"]["ru"]
            setattr(page, f"title_{lang}", title)
            setattr(page, f"seo_title_{lang}", title)
            setattr(page, f"subtitle_{lang}", "")
            setattr(page, f"seo_description_{lang}", "")
            # Keep each language body independent. Older payloads may only have
            # body_ru; the release repair command fills missing EN/KG bodies from
            # the corresponding localized WordPress pages.
            setattr(page, f"body_{lang}", item.get(f"body_{lang}", ""))

        page.template = Page.TEMPLATE_DEFAULT
        page.force_backend_render = True
        page.is_published = True
        page.data = {
            "render_mode": "default",
            "content_status": CONTENT_STATUS,
            "legacy_sources": item["sources"],
            "legacy_source_modified": item["source_modified"],
            "legacy_payload_generated_at": payload["generated_at"],
        }
        sources = ", ".join(item["sources"]) or "навигационная страница"
        page.internal_notes = (
            f"Содержимое синхронизировано с официальным сайтом ({sources}) "
            f"командой apply_legacy_parity, выгрузка от {payload['generated_at']}."
        )
        page.save()

    def apply_news(self, payload):
        changed = 0
        for external_id, title in (payload.get("news_title_fixes") or {}).items():
            changed += News.objects.filter(external_id=external_id).exclude(title_ru=title).update(title_ru=title)

        replacements = payload.get("news_en_replacements") or {}
        if replacements:
            pattern = re.compile("|".join(re.escape(key) for key in replacements))
            for news in News.objects.all():
                fields = []
                for field in ("title_en", "short_description_en", "description_en"):
                    value = getattr(news, field) or ""
                    updated = pattern.sub(lambda m: replacements[m.group(0)], value)
                    if updated != value:
                        setattr(news, field, updated)
                        fields.append(field)
                if fields:
                    news.save(update_fields=fields)
                    changed += 1
        return changed

    # -------------------------------------------------------------- finalize
    def finalize(self, payload):
        removed = 0
        pending = []
        for item in payload["pages"]:
            page = Page.objects.filter(path=item["path"]).first()
            if not page:
                continue
            body = page.body_ru or ""
            if WORDPRESS_UPLOAD_RE.search(body):
                pending.append(page.path)
                continue
            # migrate_external_media registers every embedded file as a gallery
            # image or document; on these pages the text already shows them.
            for record in list(page.media_items.exclude(media_type=PageMedia.TYPE_VIDEO)) + list(page.documents.all()):
                url = record.resolved_url
                if url and url in body:
                    record.delete()  # the file itself stays in S3
                    removed += 1
        if pending:
            raise CommandError(
                "Legacy file URLs are still embedded, run `migrate_external_media --apply --strict` first: "
                + ", ".join(pending)
            )
        self.stdout.write(self.style.SUCCESS(f"Finalize complete: removed {removed} duplicate gallery/document records."))

    # ----------------------------------------------------------------- check
    def verify(self, payload):
        problems = []
        for item in payload["pages"]:
            page = Page.objects.filter(path=item["path"]).first()
            if not page:
                problems.append(f"{item['path']}: page missing")
                continue
            if page.title_ru != item["title"]["ru"]:
                problems.append(f"{item['path']}: title differs ({page.title_ru!r})")
            if (page.data or {}).get("content_status") != CONTENT_STATUS:
                problems.append(f"{item['path']}: not synced")
            if WORDPRESS_UPLOAD_RE.search(page.body_ru or ""):
                problems.append(f"{item['path']}: legacy file URLs not moved to S3")
            if not (page.body_ru or "").strip():
                problems.append(f"{item['path']}: empty body")
        if problems:
            for problem in problems:
                self.stderr.write(problem)
            raise CommandError(f"Legacy parity check failed: {len(problems)} problem(s).")
        self.stdout.write(self.style.SUCCESS(f"Legacy parity check passed for {len(payload['pages'])} pages."))
