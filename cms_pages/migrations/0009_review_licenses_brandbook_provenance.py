from django.db import migrations


def review_document_provenance(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")

    page = Page.objects.filter(path="/university/normative-docs/licenses").first()
    if page:
        data = dict(page.data or {})
        data.pop("verified_source_urls", None)
        data.pop("verified_legacy_source", None)
        data["content_status"] = "requires-current-admin-document-verification"
        data["source_reviewed_date"] = "2026-10-17"
        page.data = data
        page.internal_notes = (
            "Старые изображения документов сохранены как исторические материалы, но их актуальность и реквизиты "
            "не должны считаться подтвержденными без проверки администрацией. Публиковать номера лицензий нужно "
            "только по актуальным оригиналам в CMS."
        )
        page.save(update_fields=["data", "internal_notes", "updated_at"])

    page = Page.objects.filter(path="/university/normative-docs/logo").first()
    if page:
        data = dict(page.data or {})
        data.pop("verified_source_urls", None)
        data.pop("verified_legacy_source", None)
        data["content_status"] = "historical-brand-assets-require-current-verification"
        data["source_reviewed_date"] = "2026-10-17"
        page.data = data
        page.internal_notes = (
            "Исторический брендбук/файлы со старого сайта можно хранить в CMS, но перед обозначением их как "
            "действующих правил бренда администрация должна подтвердить актуальную версию."
        )
        page.save(update_fields=["data", "internal_notes", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0008_correct_unverified_uncovered_content"),
    ]

    operations = [
        migrations.RunPython(review_document_provenance, migrations.RunPython.noop),
    ]
