from django.db import models

from cms_pages.models import Page
from program_pages.utils import program_scope_query


class ItCollegePageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(program_scope_query("it_college"))


class ItCollegePage(Page):
    objects = ItCollegePageManager()

    class Meta:
        proxy = True
        app_label = "it_college_pages"
        verbose_name = "Страница IT College"
        verbose_name_plural = "Страницы IT College"
