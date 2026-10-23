import html

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from cms_pages.models import Page
from tools.build_legacy_parity import Cleaner, NAV_PAGES, PAGES, fetch_all


LANGUAGES = ("en", "kg")
FIELDS = "id,slug,link,title,content,modified"


def has_meaningful_html(value):
    if not value:
        return False
    soup = BeautifulSoup(value, "html.parser")
    return bool(soup.get_text(" ", strip=True) or soup.find("img") or soup.find("a"))


class Command(BaseCommand):
    help = (
        "Repairs English/Kyrgyz bodies for legacy-parity CMS pages from the corresponding "
        "official salymbekov.com WordPress translations. Russian content is preserved."
    )

    def handle(self, *args, **options):
        self.stdout.write("Fetching localized legacy WordPress pages...")

        try:
            localized_pages = {
                lang: {item["slug"]: item for item in fetch_all("pages", lang, FIELDS)}
                for lang in LANGUAGES
            }
        except Exception as exc:
            self.stderr.write(
                self.style.WARNING(
                    f"Could not fetch legacy translations; keeping current CMS translations: {exc}"
                )
            )
            return

        cleaner = Cleaner({})
        updated_pages = 0
        missing_sources = []

        for path, slugs in PAGES.items():
            page = Page.objects.filter(path=path).first()
            if not page:
                continue

            changed_fields = []

            for lang in LANGUAGES:
                parts = []
                missing = []

                for slug in slugs:
                    source = localized_pages[lang].get(slug)
                    if not source:
                        missing.append(slug)
                        continue

                    body = cleaner.clean(source.get("content", {}).get("rendered", ""))
                    if not has_meaningful_html(body):
                        continue

                    if len(slugs) > 1:
                        translated_title = html.unescape(
                            source.get("title", {}).get("rendered", "")
                        ).strip()
                        if translated_title:
                            parts.append(f"<h2>{html.escape(translated_title)}</h2>")
                    parts.append(body)

                if missing:
                    missing_sources.append((path, lang, missing))

                localized_body = "\n".join(parts).strip()
                if localized_body:
                    field_name = f"body_{lang}"
                    if getattr(page, field_name, "") != localized_body:
                        setattr(page, field_name, localized_body)
                        changed_fields.append(field_name)

            if changed_fields:
                data = dict(page.data or {})
                data["legacy_translations_repaired"] = True
                data["legacy_translation_source"] = "salymbekov.com"
                page.data = data
                page.save(update_fields=[*changed_fields, "data", "updated_at"])
                updated_pages += 1

        # Navigation-only legacy pages have no WordPress body. Build their links
        # from the localized CMS titles instead of reusing Russian link labels.
        for path, spec in NAV_PAGES.items():
            page = Page.objects.filter(path=path).first()
            if not page:
                continue

            changed_fields = []
            for lang in LANGUAGES:
                items = []
                for target_path in spec.get("links", []):
                    target = Page.objects.filter(path=target_path).only(
                        "path", "title_ru", "title_en", "title_kg"
                    ).first()
                    if target:
                        label = getattr(target, f"title_{lang}", "") or target.title_ru or target_path
                    else:
                        label = target_path
                    items.append(
                        f'<li><a href="{html.escape(target_path, quote=True)}">'
                        f"{html.escape(label)}</a></li>"
                    )

                localized_body = f"<ul>{''.join(items)}</ul>" if items else ""
                field_name = f"body_{lang}"
                if localized_body and getattr(page, field_name, "") != localized_body:
                    setattr(page, field_name, localized_body)
                    changed_fields.append(field_name)

            if changed_fields:
                data = dict(page.data or {})
                data["legacy_translations_repaired"] = True
                data["legacy_translation_source"] = "localized CMS navigation"
                page.data = data
                page.save(update_fields=[*changed_fields, "data", "updated_at"])
                updated_pages += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Legacy translation repair complete: updated_pages={updated_pages}, "
                f"missing_source_groups={len(missing_sources)}."
            )
        )

        for path, lang, slugs in missing_sources[:20]:
            self.stderr.write(
                self.style.WARNING(f"Missing {lang} source for {path}: {', '.join(slugs)}")
            )
