from django.contrib import admin

from cms_pages.admin import BaseCmsPageAdmin

from .models import ProgramPage
from .utils import program_family_from_path, program_level_from_path


class ProgramFamilyFilter(admin.SimpleListFilter):
    title = "Семейство программ"
    parameter_name = "program_family"

    def lookups(self, request, model_admin):
        return [
            ("mfm", "MFM"),
            ("ait", "AIT"),
            ("it-college", "IT College"),
            ("postgrad", "Postgraduate"),
            ("center", "Center"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "mfm":
            return queryset.filter(path__startswith="/education/mfm")
        if value == "ait":
            return queryset.filter(path__startswith="/education/ait")
        if value == "it-college":
            return queryset.filter(path__startswith="/education/it-college")
        if value == "postgrad":
            return queryset.filter(path__startswith="/education/postgrad")
        if value == "center":
            return queryset.filter(path__startswith="/education/center")
        return queryset


class ProgramLevelFilter(admin.SimpleListFilter):
    title = "Тип страницы"
    parameter_name = "program_level"

    def lookups(self, request, model_admin):
        return [
            ("program", "Программа"),
            ("specialty", "Специальность"),
            ("department", "Подразделение"),
            ("about", "О программе"),
            ("contacts", "Контакты"),
            ("management", "Руководство"),
            ("general", "Общая страница"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "program":
            return queryset.filter(path__contains="/programs/")
        if value == "specialty":
            return queryset.filter(path__contains="/specialties/")
        if value == "department":
            return queryset.filter(path__contains="/departments/")
        if value == "about":
            return queryset.filter(path__endswith="/about")
        if value == "contacts":
            return queryset.filter(path__endswith="/contacts")
        if value == "management":
            return queryset.filter(path__regex=r"/(director|dean)$")
        if value == "general":
            return queryset.exclude(path__contains="/programs/").exclude(path__contains="/specialties/").exclude(path__contains="/departments/")
        return queryset


@admin.register(ProgramPage)
class ProgramPageAdmin(BaseCmsPageAdmin):
    list_display = [
        "admin_title",
        "program_family",
        "program_level",
        "path",
        "content_shape",
        "media_total",
        "document_total",
        "content_ready",
        "is_published",
        "updated_at",
    ]
    list_filter = [ProgramFamilyFilter, ProgramLevelFilter, "is_published", "force_backend_render", "template"]
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg", "subtitle_ru", "subtitle_en", "subtitle_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=ProgramPage.objects.values("pk"))

    @admin.display(description="Семейство")
    def program_family(self, obj):
        return program_family_from_path(obj.path)

    @admin.display(description="Тип")
    def program_level(self, obj):
        return program_level_from_path(obj.path)

    @admin.display(description="Контент")
    def content_shape(self, obj):
        return f"Секции: {obj.sections.count()} | Карточки: {obj.cards.count()} | Статистика: {obj.stats.count()}"

    @admin.display(description="Медиа")
    def media_total(self, obj):
        return obj.media_items.count()

    @admin.display(description="Документы")
    def document_total(self, obj):
        return obj.documents.count()
