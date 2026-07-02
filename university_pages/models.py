from django.db import models

from cms_pages.models import Page
from about_pages.utils import about_scope_query


class UniversityPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(about_scope_query("university"))


class UniversityPage(Page):
    objects = UniversityPageManager()

    class Meta:
        proxy = True
        app_label = "university_pages"
        verbose_name = "Страница Университета"
        verbose_name_plural = "Страницы Университета"
