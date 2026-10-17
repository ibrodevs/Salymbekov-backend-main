import json

from django.core.management.base import BaseCommand

from cms_pages.models import Page


ACTION_REQUIRED_STATUSES = {
    "verified-historical-summary-needs-current-program-update",
    "cms-navigation-index-not-legacy-copy",
    "requires-current-admin-vacancies",
    "requires-current-admin-document-verification",
    "historical-brand-assets-require-current-verification",
}


class Command(BaseCommand):
    help = "Reports CMS pages whose content provenance still requires an administrator review."

    def add_arguments(self, parser):
        parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    def handle(self, *args, **options):
        rows = []

        for page in Page.objects.all().order_by("path"):
            data = page.data or {}
            status = data.get("content_status")
            verified_sources = data.get("verified_source_urls") or []
            verified_legacy = bool(data.get("verified_legacy_source"))

            needs_review = status in ACTION_REQUIRED_STATUSES
            if not needs_review:
                continue

            rows.append(
                {
                    "path": page.path,
                    "content_status": status,
                    "verified_source_urls": verified_sources,
                    "verified_legacy_source": verified_legacy,
                    "internal_notes": page.internal_notes,
                }
            )

        payload = {
            "pages_requiring_review": len(rows),
            "pages": rows,
        }

        if options["json"]:
            self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
            return

        if not rows:
            self.stdout.write(self.style.SUCCESS("No provenance review items remain."))
            return

        self.stdout.write(
            self.style.WARNING(
                f"CMS provenance review: {len(rows)} page(s) still require administrator verification."
            )
        )
        for row in rows:
            self.stdout.write(f"REVIEW  {row['path']}")
            self.stdout.write(f"  - status: {row['content_status']}")
            for source in row["verified_source_urls"]:
                self.stdout.write(f"  - source: {source}")
