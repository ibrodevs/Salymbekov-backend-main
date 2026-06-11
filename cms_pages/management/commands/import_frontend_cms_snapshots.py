import json
from pathlib import Path
from urllib.parse import urlparse

from django.core.files import File
from django.core.management.base import BaseCommand

from cms_pages.models import Page, PageDocument, PageLink, PageMedia


DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".zip",
    ".rar",
    ".csv",
}


def is_external_url(value):
    return value.startswith("http://") or value.startswith("https://")


def is_document_url(value):
    clean_path = urlparse(value).path.lower()
    return any(clean_path.endswith(extension) for extension in DOCUMENT_EXTENSIONS)


def strip_query(value):
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return value
    return parsed.path


def resolve_frontend_asset(frontend_root, asset_url):
    clean_url = strip_query(asset_url)

    if is_external_url(clean_url):
        return None

    if clean_url.startswith("/src/assets/"):
        return frontend_root / clean_url.lstrip("/")

    if clean_url.startswith("/public/"):
        return frontend_root / clean_url.lstrip("/")

    if clean_url.startswith("/"):
        return frontend_root / "public" / clean_url.lstrip("/")

    relative_path = (frontend_root / clean_url).resolve()
    return relative_path


def deduplicate(items):
    seen = set()
    ordered = []

    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)

    return ordered


class Command(BaseCommand):
    help = "Импортирует HTML-снимки frontend CMS-страниц в backend и переносит локальные файлы в media."

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            default=None,
            help="Путь к JSON-файлу со снимками frontend. По умолчанию используется cms_pages/imports/frontend-cms-snapshots.json.",
        )
        parser.add_argument(
            "--frontend-root",
            default=None,
            help="Путь к frontend-проекту. По умолчанию используется соседний salymbekov-frontend.",
        )
        parser.add_argument(
            "--only-path",
            default=None,
            help="Импортировать только одну страницу по пути, например /university/mission.",
        )

    def handle(self, *args, **options):
        backend_root = Path(__file__).resolve().parents[3]
        frontend_root = Path(options["frontend_root"]).resolve() if options["frontend_root"] else (backend_root.parent / "salymbekov-frontend").resolve()
        input_path = Path(options["input"]).resolve() if options["input"] else (backend_root / "cms_pages" / "imports" / "frontend-cms-snapshots.json").resolve()
        only_path = options["only_path"]

        if not input_path.exists():
            self.stderr.write(self.style.ERROR(f"Файл снимков не найден: {input_path}"))
            return

        payload = json.loads(input_path.read_text(encoding="utf-8"))
        routes = payload.get("routes", [])
        snapshot_generated_at = payload.get("generated_at")

        imported = 0
        skipped = 0
        failed = 0

        for route in routes:
            route_path = route.get("path")

            if only_path and route_path != only_path:
                continue

            if route.get("status") != "ok":
                failed += 1
                self.stderr.write(self.style.WARNING(f"Пропуск {route_path}: {route.get('error', 'unknown error')}"))
                continue

            page = Page.objects.filter(path=route_path).first()
            if not page:
                skipped += 1
                self.stderr.write(self.style.WARNING(f"Страница не найдена в CMS: {route_path}"))
                continue

            languages = route.get("languages", {})
            if not languages:
                skipped += 1
                continue

            self._import_page(page, route, languages, frontend_root, snapshot_generated_at)
            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен: imported={imported}, skipped={skipped}, failed={failed}, source={input_path}"
            )
        )

    def _import_page(self, page, route, languages, frontend_root, snapshot_generated_at):
        page.sections.all().delete()
        page.cards.all().delete()
        page.stats.all().delete()
        page.media_items.all().delete()
        page.documents.all().delete()
        page.links.all().delete()

        asset_map = {}
        image_order = 0
        doc_order = 0
        link_order = 0
        hero_assigned = False

        for lang in ("ru", "en", "kg"):
            localized = languages.get(lang, {})
            setattr(page, f"title_{lang}", localized.get("title", "")[:255])
            setattr(page, f"subtitle_{lang}", localized.get("subtitle", ""))
            setattr(page, f"body_{lang}", localized.get("html", ""))
            setattr(page, f"seo_title_{lang}", localized.get("title", "")[:255])
            setattr(page, f"seo_description_{lang}", localized.get("subtitle", ""))

        page.force_backend_render = True
        page.is_published = True
        page.data = {
            **(page.data or {}),
            "render_mode": "raw_html",
            "source_component": route.get("componentName"),
            "source_module": route.get("moduleId"),
            "imported_from_frontend": True,
            "snapshot_generated_at": snapshot_generated_at,
        }
        page.internal_notes = (
            "Контент импортирован из frontend-снимка и теперь редактируется через CMS. "
            f"Исходный fallback-компонент: {route.get('componentName')}."
        )
        page.save()

        all_images = deduplicate(
            image
            for localized in languages.values()
            for image in localized.get("images", [])
            if image
        )
        anchor_map = {}
        for localized in languages.values():
            for anchor in localized.get("anchors", []):
                href = anchor.get("href", "").strip()
                text = anchor.get("text", "").strip()

                if not href:
                    continue

                if href not in anchor_map or (text and not anchor_map[href]):
                    anchor_map[href] = text

        for image_url in all_images:
            normalized_url = strip_query(image_url)

            if normalized_url in asset_map:
                continue

            image_order += 1
            media = PageMedia(page=page, media_type=PageMedia.TYPE_IMAGE, order=image_order, is_hero=not hero_assigned)
            if not hero_assigned:
                hero_assigned = True

            if is_external_url(normalized_url):
                media.external_url = normalized_url
            else:
                asset_path = resolve_frontend_asset(frontend_root, normalized_url)
                if asset_path and asset_path.exists():
                    with asset_path.open("rb") as asset_file:
                        media.file.save(asset_path.name, File(asset_file), save=False)
                else:
                    media.external_url = normalized_url

            media.save()
            asset_map[normalized_url] = media.resolved_url

        for href, text in anchor_map.items():
            normalized_href = strip_query(href)

            if is_document_url(normalized_href):
                doc_order += 1
                document = PageDocument(page=page, order=doc_order)
                document.title_ru = text[:255]
                document.title_en = text[:255]
                document.title_kg = text[:255]

                if is_external_url(normalized_href):
                    document.external_url = href
                else:
                    asset_path = resolve_frontend_asset(frontend_root, normalized_href)
                    if asset_path and asset_path.exists():
                        with asset_path.open("rb") as asset_file:
                            document.file.save(asset_path.name, File(asset_file), save=False)
                    else:
                        document.external_url = href

                document.save()
                if normalized_href not in asset_map:
                    asset_map[normalized_href] = document.resolved_url
                continue

            link_order += 1
            link = PageLink(
                page=page,
                order=link_order,
                url=href,
                external=not href.startswith("/"),
            )
            link.title_ru = text[:255]
            link.title_en = text[:255]
            link.title_kg = text[:255]
            link.save()

        for lang in ("ru", "en", "kg"):
            field_name = f"body_{lang}"
            html = getattr(page, field_name, "") or ""

            for original_url, replacement_url in asset_map.items():
                html = html.replace(f'"{original_url}"', f'"{replacement_url}"')

            setattr(page, field_name, html)

        page.save(update_fields=[
            "title_ru",
            "title_en",
            "title_kg",
            "subtitle_ru",
            "subtitle_en",
            "subtitle_kg",
            "body_ru",
            "body_en",
            "body_kg",
            "seo_title_ru",
            "seo_title_en",
            "seo_title_kg",
            "seo_description_ru",
            "seo_description_en",
            "seo_description_kg",
            "force_backend_render",
            "is_published",
            "data",
            "internal_notes",
            "updated_at",
        ])
