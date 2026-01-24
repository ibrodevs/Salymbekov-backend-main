from django.contrib import admin
from .models import Banner
from unfold.admin import ModelAdmin
# Register your models here.

@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    pass