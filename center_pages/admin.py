from django.contrib import admin

from cms_pages.admin import BaseCmsPageAdmin
from program_pages.utils import program_family_from_path, program_level_from_path

from .models import CenterPage


@admin.register(CenterPage)
class CenterPageAdmin(BaseCmsPageAdmin):
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
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=CenterPage.objects.values("pk"))

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
