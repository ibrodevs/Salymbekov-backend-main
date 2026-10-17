import json
import re
from urllib.parse import urlparse

from django.core.management.base import BaseCommand

from cms_pages.models import Page


URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
PLACEHOLDER_MARKERS = (
    "This is the about page.",
    "Here are our services.",
    "Contact us here.",
    "Положительно для малейшего ухода",
    "via.placeholder.com",
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


class Command(BaseCommand):
    help = (
        "Audits the CMS routes that already exist in the new site. Reports missing languages, "
        "known placeholder text, unresolved translation keys, old WordPress assets and "
        "other external media/document references."
    )

    def add_arguments(self, parser):
        parser.add_argument("--json", action="store_true", help="Print machine-readable JSON only.")
        parser.add_argument("--only-problems", action="store_true", help="Omit clean pages from the report.")

    def handle(self, *args, **options):
        report = []
        pages = Page.objects.all().prefetch_related("sections", "media_items", "documents", "links")

        for page in pages:
            problems = []
            external_urls = set()
            legacy_urls = set()

            for lang in ("ru", "en", "kg"):
                title = getattr(page, f"title_{lang}", "") or ""
                subtitle = getattr(page, f"subtitle_{lang}", "") or ""
                body = getattr(page, f"body_{lang}", "") or ""
                if not title.strip():
                    problems.append(f"missing_title_{lang}")
                if looks_like_translation_key(title):
                    problems.append(f"translation_key_title_{lang}:{title.strip()}")
                if not body.strip() and not page.sections.exists() and not page.media_items.exists() and not page.documents.exists():
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
                    for url in collect_urls(body):
                        external_urls.add(url)
                        if is_legacy_asset_url(url):
                            legacy_urls.add(url)

            media_external = [item.external_url for item in page.media_items.all() if item.external_url]
            docs_external = [item.external_url for item in page.documents.all() if item.external_url]
            links_external = [item.url for item in page.links.all() if item.url and item.url.startswith(("http://", "https://"))]

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
            item = {
                "path": page.path,
                "published": page.is_published,
                "problems": clean_problems,
                "legacy_urls": sorted(legacy_urls),
                "external_urls": sorted(external_urls),
                "media_count": page.media_items.count(),
                "document_count": page.documents.count(),
                "section_count": page.sections.count(),
                "verified_legacy_source": bool((page.data or {}).get("verified_legacy_source")),
            }
            if clean_problems or not options["only_problems"]:
                report.append(item)

        summary = {
            "pages_checked": Page.objects.count(),
            "pages_with_problems": sum(1 for item in report if item["problems"]),
            "pages_with_legacy_assets": sum(1 for item in report if item["legacy_urls"]),
            "report": report,
        }

        if options["json"]:
            self.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"CMS audit: pages={summary['pages_checked']}, problems={summary['pages_with_problems']}, "
                f"legacy-assets={summary['pages_with_legacy_assets']}"
            )
        )
        for item in report:
            if not item["problems"]:
                self.stdout.write(f"OK  {item['path']}")
                continue
            self.stdout.write(self.style.WARNING(f"ISSUE  {item['path']}"))
            for problem in item["problems"]:
                self.stdout.write(f"  - {problem}")
            for url in item["legacy_urls"]:
                self.stdout.write(f"    legacy: {url}")
