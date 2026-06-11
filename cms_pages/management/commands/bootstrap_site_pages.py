import re
from pathlib import Path

from django.core.management.base import BaseCommand

from cms_pages.models import Page


ROUTE_PATTERN = re.compile(r"managedPage\('([^']+)',\s*<([A-Za-z0-9_]+)")


def humanize_path(path_value):
    if path_value == "/":
        return "Главная"

    parts = [part for part in path_value.strip("/").split("/") if part]
    if not parts:
        return "Страница"

    return " / ".join(part.replace("-", " ").replace("_", " ").title() for part in parts)


class Command(BaseCommand):
    help = "Создает CMS-страницы по маршрутам, уже подключенным через ManagedPageRoute во frontend."

    def add_arguments(self, parser):
        parser.add_argument(
            "--frontend-app",
            default=None,
            help="Путь до frontend src/App.jsx. По умолчанию используется соседний проект salymbekov-frontend/src/App.jsx.",
        )
        parser.add_argument(
            "--overwrite-metadata",
            action="store_true",
            help="Перезаписывать admin_title, navigation_group и внутренние заметки даже для существующих страниц.",
        )

    def handle(self, *args, **options):
        frontend_app = options["frontend_app"]
        overwrite_metadata = options["overwrite_metadata"]

        if frontend_app:
            app_path = Path(frontend_app).resolve()
        else:
            app_path = (Path(__file__).resolve().parents[4] / "salymbekov-frontend" / "src" / "App.jsx").resolve()

        if not app_path.exists():
            self.stderr.write(self.style.ERROR(f"Файл frontend маршрутов не найден: {app_path}"))
            return

        content = app_path.read_text(encoding="utf-8")
        matches = ROUTE_PATTERN.findall(content)

        if not matches:
            self.stderr.write(self.style.WARNING("Маршруты с managedPage(...) не найдены."))
            return

        created_count = 0
        updated_count = 0

        for path_value, component_name in matches:
            default_group = path_value.strip("/").split("/")[0] if path_value.strip("/") else "main"
            defaults = {
                "admin_title": humanize_path(path_value),
                "navigation_group": default_group,
                "internal_notes": (
                    "Страница создана автоматически из frontend-маршрута. "
                    f"Исторический fallback-компонент: {component_name}."
                ),
            }

            page, created = Page.objects.get_or_create(path=path_value, defaults=defaults)
            if created:
                created_count += 1
                continue

            if overwrite_metadata:
                page.admin_title = defaults["admin_title"]
                page.navigation_group = defaults["navigation_group"]
                page.internal_notes = defaults["internal_notes"]
                page.save(update_fields=["admin_title", "navigation_group", "internal_notes", "updated_at"])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created_count} CMS-страниц, обновлено {updated_count}. Источник: {app_path}"
            )
        )

