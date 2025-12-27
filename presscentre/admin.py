from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import TabularInline
from .models import Category, News, NewsImage


class NewsImageInline(TabularInline):
    model = NewsImage
    extra = 1
    fields = ["image", "order"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["id", "title_ru", "title_en", "title_kg"]
    search_fields = ["title_ru", "title_en", "title_kg"]


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = [
        "id",
        "get_title_ru",
        "category",
        "is_recommended",
        "published_at",
        "created_at",
    ]
    list_filter = ["is_recommended", "category", "published_at"]
    search_fields = ["title_ru", "title_en", "title_kg"]
    date_hierarchy = "published_at"
    inlines = [NewsImageInline]

    def get_title_ru(self, obj):
        return obj.title_ru

    get_title_ru.short_description = "Заголовок (RU)"
