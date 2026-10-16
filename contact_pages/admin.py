from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import TabularInline

from cms_pages.admin import BaseCmsPageAdmin
from about_pages.utils import about_section_from_path

from .models import ContactPage, FooterLink, FooterSettings


@admin.register(ContactPage)
class ContactPageAdmin(BaseCmsPageAdmin):
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
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=ContactPage.objects.values("pk"))

    @admin.display(description="Раздел")
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


class FooterLinkInline(TabularInline):
    model = FooterLink
    extra = 0
    ordering = ["section", "order"]
    fields = [
        "section",
        "title_ru",
        "title_en",
        "title_kg",
        "url",
        "icon",
        "order",
        "is_active",
    ]


@admin.register(FooterSettings)
class FooterSettingsAdmin(ModelAdmin):
    inlines = [FooterLinkInline]
    list_display = ["__str__", "email", "phone", "is_active", "updated_at"]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    ("brand_ru", "brand_en", "brand_kg"),
                    ("description_ru", "description_en", "description_kg"),
                    ("address_ru", "address_en", "address_kg"),
                    "phone",
                    "email",
                    "website",
                    "is_active",
                )
            },
        ),
        (
            "Заголовки разделов",
            {
                "fields": (
                    ("quick_links_title_ru", "quick_links_title_en", "quick_links_title_kg"),
                    ("academic_title_ru", "academic_title_en", "academic_title_kg"),
                    ("social_title_ru", "social_title_en", "social_title_kg"),
                )
            },
        ),
        (
            "Copyright",
            {
                "fields": (("copyright_ru", "copyright_en", "copyright_kg"),)
            },
        ),
    )

    def has_add_permission(self, request):
        if FooterSettings.objects.exists():
            return False
        return super().has_add_permission(request)
