import importlib
import json
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand

from cms_pages.models import Page


CURATED_PATHS = {
    "/about": ("0003_repair_verified_legacy_content", "ABOUT"),
    "/university/mission": ("0003_repair_verified_legacy_content", "MISSION"),
    "/founderMessege": ("0003_repair_verified_legacy_content", "FOUNDER"),
    "/university/management/founder": ("0003_repair_verified_legacy_content", "FOUNDER"),
    "/services": ("0004_repair_services_and_contacts", "SERVICES"),
    "/contact": ("0004_repair_services_and_contacts", "CONTACTS"),
    "/contacts": ("0004_repair_services_and_contacts", "CONTACTS"),
}

CURATED_NOTES = {
    "/about": "Проверенный контент: официальные документы и стратегический план Салымбеков Университета.",
    "/university/mission": "Миссия и стратегические цели сверены с официальным стратегическим планом Университета.",
    "/founderMessege": "Проверенный официальный контент об учредителе Салымбеков Университета.",
    "/university/management/founder": "Проверенный официальный контент об учредителе Салымбеков Университета.",
    "/services": "Направления образовательной деятельности приведены к официальным документам Университета.",
    "/contact": "Контактные данные сверены с официальными публичными данными Университета.",
    "/contacts": "Контактные данные сверены с официальными публичными данными Университета.",
}


def apply_curated_content(page):
    """Apply curated payload only to a page that was empty before this command."""
    spec = CURATED_PATHS.get(page.path)
    if not spec:
        return False

    module_name, payload_name = spec
    module = importlib.import_module(f"cms_pages.migrations.{module_name}")
    payload = getattr(module, payload_name)
    apply_fn = getattr(module, "_apply_content", None) or getattr(module, "apply_content")
    apply_fn(page, payload, CURATED_NOTES[page.path])
    return True


class Command(BaseCommand):
    help = (
        "Safely fills only empty CMS pages from the saved frontend snapshots. "
        "Existing curated or administrator-edited content is never overwritten."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            default=None,
            help=(
                "Optional snapshot JSON path. Defaults to "
                "cms_pages/imports/frontend-cms-snapshots.json."
            ),
        )

    def handle(self, *args, **options):
        backend_root = Path(__file__).resolve().parents[3]
        input_path = (
            Path(options["input"]).resolve()
            if options["input"]
            else (backend_root / "cms_pages" / "imports" / "frontend-cms-snapshots.json").resolve()
        )

        if not input_path.exists():
            self.stderr.write(self.style.WARNING(f"Snapshot file not found: {input_path}"))
            return

        payload = json.loads(input_path.read_text(encoding="utf-8"))
        routes = payload.get("routes", [])
        imported = 0
        curated = 0
        preserved = 0
        unavailable = 0

        for route in routes:
            path = route.get("path")
            languages = route.get("languages") or {}
            if not path or route.get("status") != "ok" or not languages:
                unavailable += 1
                continue

            page = Page.objects.filter(path=path).first()
            if not page:
                unavailable += 1
                continue

            if page.has_meaningful_content:
                preserved += 1
                continue

            call_command(
                "import_frontend_cms_snapshots",
                "--input",
                str(input_path),
                "--only-path",
                path,
            )

            page.refresh_from_db()
            if apply_curated_content(page):
                curated += 1
            else:
                data = dict(page.data or {})
                data.setdefault("content_status", "frontend-snapshot-imported-needs-source-parity-review")
                data.setdefault("snapshot_fill_safe", True)
                page.data = data
                page.internal_notes = (
                    (page.internal_notes or "")
                    + "\nАвтоматически заполнено только потому, что CMS-страница была пустой. "
                      "Существующий проверенный или вручную отредактированный контент не перезаписывается."
                ).strip()
                page.save(update_fields=["data", "internal_notes", "updated_at"])
            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Empty CMS snapshot fill complete: "
                f"imported={imported}, curated={curated}, preserved={preserved}, unavailable={unavailable}."
            )
        )
