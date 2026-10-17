import json
import re
from urllib.parse import urlparse

from django.core.management.base import BaseCommand

from cms_pages.models import Page
from cms_pages.site_routes import CMS_PAGE_PATHS


URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
PLACEHOLDER_MARKERS = (
    "This is the about page.",
    "Here are our services.",
    "Contact us here.",
    "Положительно для малейшего ухода",
    "via.placeholder.com",
    "XXX-XX-XX",
    "№123456789",
    "№987654321",
    "№456789123",
)
TRANSLATION_KEY_PREFIXES = (
    "navbar.",
    "mission.",
    "rector.",
    "aboutAIT.",
    "lawsRegulations.",
)
LEGACY_HOSTS = {"salymbekov.com", "www.salymbekov.com"}


def collect_urls(value):
    if not value:
        return set()
    return {item.rstrip(".,;:)]}") for item in URL_RE.findall(str(value))}


def is_legacy_asset_url(url):
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        path = parsed.path.lower()
    except ValueError:
        return False
    return host in LEGACY_HOSTS and path.startswith("/wp-content/")


def looks_like_translation_key(value):
    clean = (value or "").strip()
    return any(clean.startswith(prefix) for prefix in TRANSLATION_KEY_PREFIXES)


def missing_page_item(path):
    return {
        "path": path,
        "published": False,
        "problems": ["missing_page_record"],
        "legacy_urls": [],
        "external_urls": [],
        "media_count": 0,
        "document_count": 0,
        "section_count": 0,
        "verified_legacy_source": False,
    }


class Command(BaseCommand):
    help = (
        "Audits every canonical CMS route. Reports missing Page rows, missing languages, "
        "known placeholder text, unresolved translation keys, old WordPress assets and "
        "external media/document references."
    )

    def add_arguments(self, parser):
        parser.add_argument("--json", action="store_true", help="Print machine-readable JSON only.")
        parser.add_argument("--only-problems", action="store_true", help="Omit clean pages from the report.")

    def handle(self, *args, **options):
        report = []
        pages = list(
            Page.objects.all().prefetch_related(
                "sections", "media_items", "documents", "links"
            )
        )
        existing_paths = {page.path for page in pages}
        missing_paths = sorted(set(CMS_PAGE_PATHS) - existing_paths)

        for path in missing_paths:
            report.append(missing_page_item(path))

        for page in pages:
            problems = []
            external_urls = set()
            legacy_urls = set()
            has_structured_content = bool(
                page.sections.all()
                or page.media_items.all()
                or page.documents.all()
            )

            for lang in ("ru", "en", "kg"):
                title = getattr(page, f"title_{lang}", "") or ""
                subtitle = getattr(page, f"subtitle_{lang}", "") or ""
                body = getattr(page, f"body_{lang}", "") or ""
                if not title.strip():
                    problems.append(f"missing_title_{lang}")
                if looks_like_translation_key(title):
                    problems.append(f"translation_key_title_{lang}:{title.strip()}")
                if not body.strip() and not has_structured_content:
                    problems.append(f"missing_content_{lang}")

                combined = f"{title}\n{subtitle}\n{body}"
                for marker in PLACEHOLDER_MARKERS:
                    if marker.lower() in combined.lower():
                        problems.append(f"placeholder:{marker}")

                for url in collect_urls(combined):
                    external_urls.add(url)
                    if is_legacy_asset_url(url):
                        legacy_urls.add(url)

            try:
                serialized_data = json.dumps(page.data or {}, ensure_ascii=False)
            except (TypeError, ValueError):
                serialized_data = ""
            for marker in PLACEHOLDER_MARKERS:
                if marker.lower() in serialized_data.lower():
                    problems.append(f"placeholder:{marker}")
            for url in collect_urls(serialized_data):
                external_urls.add(url)
                if is_legacy_asset_url(url):
                    legacy_urls.add(url)

            for section in page.sections.all():
                for lang in ("ru", "en", "kg"):
                    body = getattr(section, f"body_{lang}", "") or ""
                    for marker in PLACEHOLDER_MARKERS:
                        if marker.lower() in body.lower():
                            problems.append(f"placeholder:{marker}")
                    for url in collect_urls(body):
                        external_urls.add(url)
                        if is_legacy_asset_url(url):
                            legacy_urls.add(url)

            media_external = [
                item.external_url
                for item in page.media_items.all()
                if item.external_url
            ]
            docs_external = [
                item.external_url
                for item in page.documents.all()
                if item.external_url
            ]
            links_external = [
                item.url
                for item in page.links.all()
                if item.url and item.url.startswith(("http://", "https://"))
            ]

            for url in [*media_external, *docs_external, *links_external]:
                external_urls.add(url)
                if is_legacy_asset_url(url):
                    legacy_urls.add(url)

            if legacy_urls:
                problems.append(f"legacy_wordpress_assets:{len(legacy_urls)}")
            if media_external:
                problems.append(f"external_media_records:{len(media_external)}")
            if docs_external:
                problems.append(f"external_document_records:{len(docs_external)}")

            clean_problems = list(dict.fromkeys(problems))
            page_data = page.data or {}
            item = {
                "path": page.path,
                "published": page.is_published,
                "problems": clean_problems,
                "legacy_urls": sorted(legacy_urls),
                "external_urls": sorted(external_urls),
                "media_count": page.media_items.count(),
                "document_count": page.documents.count(),
                "section_count": page.sections.count(),
                "verified_legacy_source": bool(
                    page_data.get("verified_legacy_source")
                    or page_data.get("verified_source_urls")
                ),
            }
            if clean_problems or not options["only_problems"]:
                report.append(item)

        problem_count = sum(1 for item in report if item["problems"])
        summary = {
            "expected_routes": len(CMS_PAGE_PATHS),
            "pages_checked": len(pages),
            "missing_page_records": len(missing_paths),
            "pages_with_problems": problem_count,
            "pages_with_legacy_assets": sum(
                1 for item in report if item["legacy_urls"]
            ),
            "report": sorted(report, key=lambda item: item["path"]),
        }

        if options["json"]:
            self.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2))
            return

        self.stdout.write(
            self.style.SUCCESS(
                "CMS audit: "
                f"expected={summary['expected_routes']}, "
                f"pages={summary['pages_checked']}, "
                f"missing={summary['missing_page_records']}, "
                f"problems={summary['pages_with_problems']}, "
                f"legacy-assets={summary['pages_with_legacy_assets']}"
            )
        )
        for item in summary["report"]:
            if not item["problems"]:
                self.stdout.write(f"OK  {item['path']}")
                continue
            self.stdout.write(self.style.WARNING(f"ISSUE  {item['path']}"))
            for problem in item["problems"]:
                self.stdout.write(f"  - {problem}")
            for url in item["legacy_urls"]:
                self.stdout.write(f"    legacy: {url}")
