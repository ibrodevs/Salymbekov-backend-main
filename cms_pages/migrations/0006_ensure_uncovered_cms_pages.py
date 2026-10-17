from importlib import import_module

from django.core.management import call_command
from django.db import migrations


PAGE_METADATA = {
    "/university/quality-management-system/quality-monitoring": ("Мониторинг качества", "university"),
    "/university/management/public-councils": ("Общественные советы", "university"),
    "/education/it-college/double-diploma": ("Программа двойного диплома", "education"),
    "/clinical/simulation-center": ("Симуляционный центр", "clinical"),
    "/vacancies": ("Вакансии", "main"),
    "/university/normative-docs/licenses": ("Лицензии и свидетельства", "university"),
    "/university/normative-docs/logo": ("Брендбук", "university"),
}


def ensure_uncovered_pages(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")
    PageMedia = apps.get_model("cms_pages", "PageMedia")
    PageDocument = apps.get_model("cms_pages", "PageDocument")
    source_migration = import_module("cms_pages.migrations.0005_repair_uncovered_cms_pages")

    created_paths = set()

    for path, (payload, source_urls) in source_migration.PAGES.items():
        admin_title, navigation_group = PAGE_METADATA[path]
        page, created = Page.objects.get_or_create(
            path=path,
            defaults={
                "admin_title": admin_title,
                "navigation_group": navigation_group,
                "internal_notes": "CMS-only страница создана миграцией, потому что frontend bootstrap недоступен на Heroku.",
            },
        )
        if not created:
            continue

        source_migration.apply_content(page, payload, source_urls)
        created_paths.add(path)

    licenses_path = "/university/normative-docs/licenses"
    if licenses_path in created_paths:
        licenses = Page.objects.get(path=licenses_path)
        PageMedia.objects.create(
            page=licenses,
            media_type="image",
            external_url="https://salymbekov.com/wp-content/uploads/2021/04/img4-rotated.jpg",
            is_hero=False,
            order=10,
            title_ru="Лицензия / свидетельство",
            title_en="Licence / certificate",
            title_kg="Лицензия / күбөлүк",
            alt_text_ru="Официальный документ Салымбеков Университета",
            alt_text_en="Official Salymbekov University document",
            alt_text_kg="Салымбеков Университетинин расмий документи",
        )

    brandbook_path = "/university/normative-docs/logo"
    if brandbook_path in created_paths:
        brandbook = Page.objects.get(path=brandbook_path)
        PageDocument.objects.create(
            page=brandbook,
            external_url="https://salymbekov.com/wp-content/uploads/2023/10/brjendbuk_organized_new.pdf",
            order=10,
            title_ru="Брендбук Салымбеков Университета",
            title_en="Salymbekov University Brandbook",
            title_kg="Салымбеков Университетинин брендбугу",
        )

    if created_paths.intersection({licenses_path, brandbook_path}):
        try:
            call_command("migrate_external_media", "--apply", "--timeout", "15")
        except Exception as exc:
            print(f"Final media copy for newly created CMS pages skipped/partial: {exc}")


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0005_repair_uncovered_cms_pages"),
    ]

    operations = [
        migrations.RunPython(ensure_uncovered_pages, migrations.RunPython.noop),
    ]
