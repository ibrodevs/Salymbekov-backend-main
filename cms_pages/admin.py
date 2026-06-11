from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import StackedInline, TabularInline

from .models import Page, PageCard, PageDocument, PageLink, PageMedia, PageSection, PageStat


class PageSectionInline(StackedInline):
    model = PageSection
    extra = 0
    ordering = ["order"]


class PageCardInline(StackedInline):
    model = PageCard
    extra = 0
    ordering = ["order"]


class PageStatInline(TabularInline):
    model = PageStat
    extra = 0
    ordering = ["order"]


class PageMediaInline(TabularInline):
    model = PageMedia
    extra = 0
    ordering = ["order"]


class PageDocumentInline(TabularInline):
    model = PageDocument
    extra = 0
    ordering = ["order"]


class PageLinkInline(TabularInline):
    model = PageLink
    extra = 0
    ordering = ["order"]


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = [
        "admin_title",
        "path",
        "navigation_group",
        "template",
        "content_ready",
        "is_published",
        "force_backend_render",
        "updated_at",
    ]
    list_filter = ["is_published", "force_backend_render", "template", "navigation_group"]
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg"]
    ordering = ["navigation_group", "admin_title", "path"]
    inlines = [
        PageSectionInline,
        PageCardInline,
        PageStatInline,
        PageMediaInline,
        PageDocumentInline,
        PageLinkInline,
    ]
    fieldsets = (
        (
            "Маршрут и публикация",
            {
                "fields": (
                    "admin_title",
                    "path",
                    "navigation_group",
                    "template",
                    "is_published",
                    "force_backend_render",
                )
            },
        ),
        (
            "Заголовок и описание",
            {
                "fields": (
                    ("title_ru", "title_en", "title_kg"),
                    ("subtitle_ru", "subtitle_en", "subtitle_kg"),
                )
            },
        ),
        (
            "Основной текст",
            {
                "fields": (
                    "body_ru",
                    "body_en",
                    "body_kg",
                )
            },
        ),
        (
            "SEO",
            {
                "classes": ("tab",),
                "fields": (
                    ("seo_title_ru", "seo_title_en", "seo_title_kg"),
                    ("seo_description_ru", "seo_description_en", "seo_description_kg"),
                ),
            },
        ),
        (
            "Расширенные настройки",
            {
                "classes": ("tab",),
                "fields": ("data", "internal_notes"),
            },
        ),
    )

    @admin.display(boolean=True, description="Контент готов")
    def content_ready(self, obj):
        return obj.has_meaningful_content
