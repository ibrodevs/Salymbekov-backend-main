from django.db import models

from cms_pages.models import Page
from program_pages.utils import program_scope_query


class MfmPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(program_scope_query("mfm"))


class MfmPage(Page):
    objects = MfmPageManager()

    class Meta:
        proxy = True
        app_label = "mfm_pages"
        verbose_name = "Страница MFM"
        verbose_name_plural = "Страницы MFM"
