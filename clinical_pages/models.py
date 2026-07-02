from django.db import models

from cms_pages.models import Page
from about_pages.utils import about_scope_query


class ClinicalPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(about_scope_query("clinical"))


class ClinicalPage(Page):
    objects = ClinicalPageManager()

    class Meta:
        proxy = True
        app_label = "clinical_pages"
        verbose_name = "Страница клинической базы"
        verbose_name_plural = "Страницы клинической базы"
