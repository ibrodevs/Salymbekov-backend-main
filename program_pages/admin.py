from django.contrib import admin

from cms_pages.admin import BaseCmsPageAdmin

from .models import ProgramPage


@admin.register(ProgramPage)
class ProgramPageAdmin(BaseCmsPageAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(pk__in=ProgramPage.objects.values("pk"))
