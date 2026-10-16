from django.core.management import call_command
from django.db import migrations


def cleanup_legacy_wordpress_media(apps, schema_editor):
    try:
        call_command("migrate_external_media", "--apply", "--timeout", "15")
    except Exception as exc:
        # Do not block the release if a legacy remote asset is unavailable.
        print(f"Legacy media cleanup skipped/partial: {exc}")


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cleanup_legacy_wordpress_media, migrations.RunPython.noop),
    ]
