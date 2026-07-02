from django.contrib import admin

from cms_pages.admin import BaseCmsPageAdmin

from .models import AboutPage
from .utils import about_section_from_path


class AboutSectionFilter(admin.SimpleListFilter):
    title = "Подраздел"
    parameter_name = "about_section"

    def lookups(self, request, model_admin):
        return [
            ("main", "Главная страница раздела"),
            ("university", "Университет"),
            ("clinical", "Клиническая база"),
            ("infrastructure", "Инфраструктура"),
            ("cooperation", "Сотрудничество"),
            ("contacts", "Контакты"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "main":
            return queryset.filter(path="/about")
        if value == "university":
            return queryset.filter(path__startswith="/university/")
        if value == "clinical":
            return queryset.filter(path__startswith="/clinical/")
        if value == "infrastructure":
            return queryset.filter(path__startswith="/infrastructure/")
        if value == "cooperation":
            return queryset.filter(path__startswith="/cooperation/")
        if value == "contacts":
            return queryset.filter(path__startswith="/contact") | queryset.filter(path__startswith="/contacts")
        return queryset


@admin.register(AboutPage)
class AboutPageAdmin(BaseCmsPageAdmin):
    list_display = [
        "admin_title",
        "about_section",
        "path",
        "content_shape",
        "media_total",
        "document_total",
        "content_ready",
        "is_published",
        "updated_at",
    ]
    list_filter = [AboutSectionFilter, "is_published", "force_backend_render", "template"]
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg", "subtitle_ru", "subtitle_en", "subtitle_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=AboutPage.objects.values("pk"))

    @admin.display(description="Подраздел")
    def about_section(self, obj):
        return about_section_from_path(obj.path)

    @admin.display(description="Контент")
    def content_shape(self, obj):
        return f"Секции: {obj.sections.count()} | Карточки: {obj.cards.count()} | Статистика: {obj.stats.count()}"

    @admin.display(description="Медиа")
    def media_total(self, obj):
        return obj.media_items.count()

    @admin.display(description="Документы")
    def document_total(self, obj):
        return obj.documents.count()
