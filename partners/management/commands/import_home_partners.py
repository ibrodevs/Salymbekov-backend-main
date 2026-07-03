from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from partners.models import Partner


PARTNER_SPECS = [
    {"filename": "lincoln.webp", "name": "Lincoln University College"},
    {"filename": "inti.png", "name": "INTI International University"},
    {"filename": "spbpu.jpg", "name": "Санкт-Петербургский политехнический университет Петра Великого"},
    {"filename": "paichai.png", "name": "Pai Chai University"},
    {"filename": "chungang.png", "name": "Chung-Ang University"},
    {"filename": "vision-jeonju.png", "name": "Vision College of Jeonju"},
    {"filename": "kyungdong.png", "name": "Kyungdong University"},
    {"filename": "kicb.png", "name": "KICB"},
    {"filename": "bai-tushum.jpeg", "name": "Банк Бай-Тушум"},
    {"filename": "rkdf.png", "name": "Российско-Кыргызский фонд развития"},
]


class Command(BaseCommand):
    help = "Imports homepage partner logos from the frontend public assets into backend storage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-dir",
            default=None,
            help="Directory containing the homepage partner logo files.",
        )

    def handle(self, *args, **options):
        default_source_dir = (
            Path(__file__).resolve().parents[4] / "salymbekov-frontend" / "public" / "partners"
        )
        source_dir = Path(options["source_dir"] or default_source_dir).resolve()

        if not source_dir.exists():
            raise CommandError(f"Partner logo directory not found: {source_dir}")

        created = 0
        updated = 0

        for spec in PARTNER_SPECS:
            file_path = source_dir / spec["filename"]
            if not file_path.exists():
                raise CommandError(f"Missing partner logo file: {file_path}")

            partner, partner_created = Partner.objects.get_or_create(
                name_ru=spec["name"],
                defaults={
                    "name_en": spec["name"],
                    "name_kg": spec["name"],
                    "description_ru": "",
                    "description_en": "",
                    "description_kg": "",
                },
            )

            changed = False
            if partner.name_en != spec["name"]:
                partner.name_en = spec["name"]
                changed = True
            if partner.name_kg != spec["name"]:
                partner.name_kg = spec["name"]
                changed = True

            with file_path.open("rb") as fh:
                partner.logo.save(spec["filename"], File(fh), save=False)
            changed = True

            if changed:
                partner.save()

            if partner_created:
                created += 1
            else:
                updated += 1

            self.stdout.write(f"Imported {spec['name']}")

        self.stdout.write(
            self.style.SUCCESS(f"Partner import complete. Created: {created}, updated: {updated}")
        )
