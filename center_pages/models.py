from django.db import models

from cms_pages.models import Page
from program_pages.utils import program_scope_query


class CenterPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(program_scope_query("center"))


class CenterPage(Page):
    objects = CenterPageManager()

    class Meta:
        proxy = True
        app_label = "center_pages"
        verbose_name = "Страница Center"
        verbose_name_plural = "Страницы Center"
