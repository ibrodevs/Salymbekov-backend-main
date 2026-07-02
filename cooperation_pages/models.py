from django.db import models

from cms_pages.models import Page
from about_pages.utils import about_scope_query


class CooperationPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(about_scope_query("cooperation"))


class CooperationPage(Page):
    objects = CooperationPageManager()

    class Meta:
        proxy = True
        app_label = "cooperation_pages"
        verbose_name = "Страница сотрудничества"
        verbose_name_plural = "Страницы сотрудничества"
