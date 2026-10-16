import re
from pathlib import Path

from django.core.management.base import BaseCommand

from cms_pages.models import Page


MANAGED_ROUTE_PATTERN = re.compile(
    r"managedPage\(\s*(['\"])(.*?)\1\s*,\s*<([A-Za-z0-9_]+)",
    re.MULTILINE,
)
CMS_ONLY_ROUTE_PATTERN = re.compile(
    r"cmsOnlyPage\(\s*(['\"])(.*?)\1\s*\)",
    re.MULTILINE,
)
HOME_CMS_ROUTE_PATTERN = re.compile(
    r"<Route\s+path=(['\"])(/)\1\s+element=\{<HomeCmsPage\b",
    re.MULTILINE,
)


def humanize_path(path_value):
    if path_value == "/":
        return "Главная"

    parts = [part for part in path_value.strip("/").split("/") if part]
    if not parts:
        return "Страница"

    return " / ".join(part.replace("-", " ").replace("_", " ").title() for part in parts)


def collect_cms_routes(source):
    routes = {}

    for match in MANAGED_ROUTE_PATTERN.finditer(source):
        path_value = match.group(2)
        routes[path_value] = {
            "path": path_value,
            "component": match.group(3),
            "mode": "managed",
        }

    for match in CMS_ONLY_ROUTE_PATTERN.finditer(source):
        path_value = match.group(2)
        routes[path_value] = {
            "path": path_value,
            "component": None,
            "mode": "cms-only",
        }

    for match in HOME_CMS_ROUTE_PATTERN.finditer(source):
        path_value = match.group(2)
        routes[path_value] = {
            "path": path_value,
            "component": "HomeCmsPage",
            "mode": "cms-only",
        }

    return list(routes.values())


class Command(BaseCommand):
    help = "Создает CMS-страницы по маршрутам, подключенным через managedPage/cmsOnlyPage во frontend."

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
        routes = collect_cms_routes(content)

        if not routes:
            self.stderr.write(self.style.WARNING("CMS-маршруты managedPage(...) / cmsOnlyPage(...) не найдены."))
            return

        created_count = 0
        updated_count = 0
        managed_count = 0
        cms_only_count = 0

        for route in routes:
            path_value = route["path"]
            component_name = route["component"]
            mode = route["mode"]

            if mode == "managed":
                managed_count += 1
            else:
                cms_only_count += 1

            default_group = path_value.strip("/").split("/")[0] if path_value.strip("/") else "main"
            source_note = (
                f"Исторический fallback-компонент: {component_name}."
                if component_name and mode == "managed"
                else "Frontend использует CMS-only маршрут без статического fallback-контента."
            )
            defaults = {
                "admin_title": humanize_path(path_value),
                "navigation_group": default_group,
                "internal_notes": f"Страница создана автоматически из frontend-маршрута. {source_note}",
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
                "Готово: "
                f"маршрутов={len(routes)} (managed={managed_count}, cms-only={cms_only_count}), "
                f"создано={created_count}, обновлено={updated_count}. Источник: {app_path}"
            )
        )
