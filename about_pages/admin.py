from django.contrib import admin

from cms_pages.admin import BaseCmsPageAdmin

from .models import AboutPage


@admin.register(AboutPage)
class AboutPageAdmin(BaseCmsPageAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=AboutPage.objects.values("pk"))

