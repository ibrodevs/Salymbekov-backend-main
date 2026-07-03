from django.contrib import admin

from unfold.admin import ModelAdmin

from banners.models import Banner
from cms_pages.admin import BaseCmsPageAdmin
from partners.models import Partner

from .forms import HomePageAdminForm
from .models import HomeBanner, HomeFounderPage, HomeGalleryPage, HomePage, HomePartner


@admin.register(HomePage)
class HomePageAdmin(BaseCmsPageAdmin):
    form = HomePageAdminForm
    list_display = [
        "admin_title",
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
    readonly_fields = ["path", "navigation_group", "template", "data"]
    inlines = []
    fieldsets = (
        (
            "Главная страница",
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
            "Главный текст страницы",
            {
                "fields": (
                    ("title_ru", "title_en", "title_kg"),
                    ("subtitle_ru", "subtitle_en", "subtitle_kg"),
                    "body_ru",
                    "body_en",
                    "body_kg",
                )
            },
        ),
        (
            "Отображение блоков",
            {
                "fields": (
                    ("show_hero", "show_news", "show_partners", "show_video"),
                    ("founder_page_path", "gallery_page_path"),
                )
            },
        ),
        (
            "Блок партнеров",
            {
                "fields": (
                    ("partners_badge_ru", "partners_badge_en", "partners_badge_kg"),
                    ("partners_title_ru", "partners_title_en", "partners_title_kg"),
                    "partners_subtitle_ru",
                    "partners_subtitle_en",
                    "partners_subtitle_kg",
                )
            },
        ),
        (
            "Видео-блок",
            {
                "fields": (
                    "video_url",
                    ("video_platform_label_ru", "video_platform_label_en", "video_platform_label_kg"),
                )
            },
        ),
        (
            "SEO и заметки",
            {
                "classes": ("tab",),
                "fields": (
                    ("seo_title_ru", "seo_title_en", "seo_title_kg"),
                    ("seo_description_ru", "seo_description_en", "seo_description_kg"),
                    "internal_notes",
                    "data",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=HomePage.objects.values("pk"))

    @admin.display(description="Контент")
    def content_shape(self, obj):
        return f"Секции: {obj.sections.count()} | Карточки: {obj.cards.count()} | Статистика: {obj.stats.count()}"

    @admin.display(description="Медиа")
    def media_total(self, obj):
        return obj.media_items.count()

    @admin.display(description="Документы")
    def document_total(self, obj):
        return obj.documents.count()


@admin.register(HomeFounderPage)
class HomeFounderPageAdmin(BaseCmsPageAdmin):
    list_display = ["admin_title", "path", "media_total", "content_ready", "is_published", "updated_at"]
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=HomeFounderPage.objects.values("pk"))

    @admin.display(description="Медиа")
    def media_total(self, obj):
        return obj.media_items.count()


@admin.register(HomeGalleryPage)
class HomeGalleryPageAdmin(BaseCmsPageAdmin):
    list_display = ["admin_title", "path", "media_total", "content_ready", "is_published", "updated_at"]
    search_fields = ["admin_title", "path", "title_ru", "title_en", "title_kg"]
    ordering = ["path"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=HomeGalleryPage.objects.values("pk"))

    @admin.display(description="Медиа")
    def media_total(self, obj):
        return obj.media_items.count()


@admin.register(HomeBanner)
class HomeBannerAdmin(ModelAdmin):
    list_display = ["id", "image"]
    ordering = ["id"]

    def get_queryset(self, request):
        return Banner.objects.all()


@admin.register(HomePartner)
class HomePartnerAdmin(ModelAdmin):
    list_display = ["id", "name_ru", "name_en", "name_kg"]
    list_display_links = ["id", "name_ru"]
    search_fields = ["name_ru", "name_en", "name_kg"]
    ordering = ["id"]
    fields = [
        "logo",
        "name_ru", "name_en", "name_kg",
        "description_ru", "description_en", "description_kg",
        "coord1", "coord2",
    ]

    def get_queryset(self, request):
        return Partner.objects.all()
