from django.contrib import admin
from .models import Category, News, Publication, PublicationCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title_ru", "title_en", "title_kg"]
    search_fields = ["title_ru", "title_en", "title_kg"]


@admin.register(PublicationCategory)
class PublicationCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title_ru", "title_en", "title_kg"]
    search_fields = ["title_ru", "title_en", "title_kg"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_title_ru",
        "category",
        "is_recommended",
        "is_banner",
        "published_at",
        "created_at",
    ]
    list_filter = ["is_recommended", "is_banner", "category", "published_at"]
    search_fields = ["title_ru", "title_en", "title_kg"]
    date_hierarchy = "published_at"

    def get_title_ru(self, obj):
        return obj.title_ru

    get_title_ru.short_description = "Заголовок (RU)"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ["id", "get_title_ru", "author", "published_at", "category"]
    list_filter = ["published_at", "category"]
    search_fields = ["title_ru", "title_en", "title_kg", "author"]

    fieldsets = (
        ("Категория", {"fields": ("category",)}),
        ("Заголовок", {"fields": ("title_ru", "title_en", "title_kg")}),
        (
            "Краткое описание",
            {
                "fields": (
                    "short_description_ru",
                    "short_description_en",
                    "short_description_kg",
                )
            },
        ),
        (
            "Полное описание",
            {
                "fields": ("description_ru", "description_en", "description_kg"),
                "classes": ("collapse",),
            },
        ),
        ("Автор и файл", {"fields": ("author", "pdf_file")}),
        ("Даты", {"fields": ("published_at",)}),
    )

    def get_title_ru(self, obj):
        return obj.title_ru

    get_title_ru.short_description = "Заголовок (RU)"
