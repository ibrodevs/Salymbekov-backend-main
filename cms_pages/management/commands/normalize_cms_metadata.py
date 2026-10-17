import json

from django.core.management.base import BaseCommand

from cms_pages.models import Page


PAGE_TITLES = {
    "/MaterialBaseGallery": {
        "ru": "Материально-техническая база",
        "en": "Material and Technical Base",
        "kg": "Материалдык-техникалык база",
    },
    "/science/events/conferences": {
        "ru": "Конференции",
        "en": "Conferences",
        "kg": "Конференциялар",
    },
    "/university/councils/development-council": {
        "ru": "Совет по развитию",
        "en": "Development Council",
        "kg": "Өнүктүрүү кеңеши",
    },
    "/university/structure/it-college": {
        "ru": "IT Колледж",
        "en": "IT College",
        "kg": "IT Колледж",
    },
}

CONFERENCE_COPY = {
    "ru": "Научные конференции и семинары",
    "en": "Scientific conferences and seminars",
    "kg": "Илимий конференциялар жана семинарлар",
}

BAD_VALUES = {
    "Положительно для малейшего ухода",
}


def remove_bad_fragments(value):
    updated = value or ""
    for bad_value in BAD_VALUES:
        updated = updated.replace(bad_value, "")
    return updated


class Command(BaseCommand):
    help = (
        "Fills known missing CMS metadata in RU/EN/KG and removes known snapshot "
        "placeholders. Existing meaningful administrator content is preserved."
    )

    def handle(self, *args, **options):
        changed_pages = 0

        for path, titles in PAGE_TITLES.items():
            page = Page.objects.filter(path=path).first()
            if not page:
                self.stderr.write(self.style.WARNING(f"Missing CMS page: {path}"))
                continue

            update_fields = []
            for lang in ("ru", "en", "kg"):
                title_field = f"title_{lang}"
                current_title = getattr(page, title_field, "") or ""
                cleaned_title = remove_bad_fragments(current_title).strip()
                if not cleaned_title:
                    cleaned_title = titles[lang]
                if cleaned_title != current_title:
                    setattr(page, title_field, cleaned_title)
                    update_fields.append(title_field)

                for field_prefix in ("subtitle", "body"):
                    field_name = f"{field_prefix}_{lang}"
                    current = getattr(page, field_name, "") or ""
                    cleaned = remove_bad_fragments(current)
                    if cleaned != current:
                        setattr(page, field_name, cleaned)
                        update_fields.append(field_name)

            if path == "/science/events/conferences":
                for lang in ("ru", "en", "kg"):
                    body_field = f"body_{lang}"
                    if not (getattr(page, body_field, "") or "").strip():
                        setattr(page, body_field, CONFERENCE_COPY[lang])
                        update_fields.append(body_field)

            serialized = json.dumps(page.data or {}, ensure_ascii=False)
            updated_serialized = remove_bad_fragments(serialized)
            if updated_serialized != serialized:
                page.data = json.loads(updated_serialized)
                update_fields.append("data")

            if update_fields:
                unique_fields = list(dict.fromkeys(update_fields))
                page.save(update_fields=[*unique_fields, "updated_at"])
                changed_pages += 1
                self.stdout.write(f"Updated metadata: {path} ({', '.join(unique_fields)})")

        self.stdout.write(self.style.SUCCESS(f"CMS metadata normalization complete: changed={changed_pages}."))
