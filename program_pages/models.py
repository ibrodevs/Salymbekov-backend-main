from django.db import models

from cms_pages.models import Page
from .utils import program_scope_query


class ProgramPageQuerySet(models.QuerySet):
    def for_admin(self):
        return self.filter(
            program_scope_query("mfm", "ait", "it_college", "postgrad", "center")
        )


class ProgramPageManager(models.Manager):
    def get_queryset(self):
        return ProgramPageQuerySet(self.model, using=self._db).for_admin()


class ProgramPage(Page):
    objects = ProgramPageManager()

    class Meta:
        proxy = True
        app_label = "program_pages"
        verbose_name = "Страница раздела Программы"
        verbose_name_plural = "Страницы раздела Программы"
