from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Partner


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ['id', 'name_ru', 'name_en', 'name_kg']
    list_display_links = ['id', 'name_ru']
    search_fields = ['name_ru', 'name_en', 'name_kg']
    list_filter = ['name_ru']
    fields = [
        'logo',
        'name_ru', 'name_en', 'name_kg',
        'description_ru', 'description_en', 'description_kg',
        'coord1', 'coord2'
    ]
