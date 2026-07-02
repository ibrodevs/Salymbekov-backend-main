from django.db import models

from cms_pages.models import Page
from program_pages.utils import program_scope_query


class PostgradPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(program_scope_query("postgrad"))


class PostgradPage(Page):
    objects = PostgradPageManager()

    class Meta:
        proxy = True
        app_label = "postgrad_pages"
        verbose_name = "Страница Postgraduate"
        verbose_name_plural = "Страницы Postgraduate"
