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

BAD_VALUES = {
    "Положительно для малейшего ухода",
}


class Command(BaseCommand):
    help = (
        "Fills known missing CMS page titles in RU/EN/KG and removes a known "
        "snapshot placeholder. Existing meaningful administrator content is preserved."
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
                field_name = f"title_{lang}"
                current = (getattr(page, field_name, "") or "").strip()
                if not current or current in BAD_VALUES:
                    setattr(page, field_name, titles[lang])
                    update_fields.append(field_name)

            # A bad machine-generated snapshot phrase must never be shown as body copy.
            for lang in ("ru", "en", "kg"):
                field_name = f"body_{lang}"
                current = (getattr(page, field_name, "") or "").strip()
                if current in BAD_VALUES:
                    setattr(page, field_name, "")
                    update_fields.append(field_name)

            if update_fields:
                page.save(update_fields=[*update_fields, "updated_at"])
                changed_pages += 1
                self.stdout.write(f"Updated metadata: {path} ({', '.join(update_fields)})")

        self.stdout.write(self.style.SUCCESS(f"CMS metadata normalization complete: changed={changed_pages}."))
