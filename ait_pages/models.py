from django.db import models

from cms_pages.models import Page
from program_pages.utils import program_scope_query


class AitPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(program_scope_query("ait"))


class AitPage(Page):
    objects = AitPageManager()

    class Meta:
        proxy = True
        app_label = "ait_pages"
        verbose_name = "Страница AIT"
        verbose_name_plural = "Страницы AIT"
