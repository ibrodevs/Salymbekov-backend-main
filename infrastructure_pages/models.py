from django.db import models

from cms_pages.models import Page
from about_pages.utils import about_scope_query


class InfrastructurePageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(about_scope_query("infrastructure"))


class InfrastructurePage(Page):
    objects = InfrastructurePageManager()

    class Meta:
        proxy = True
        app_label = "infrastructure_pages"
        verbose_name = "Страница инфраструктуры"
        verbose_name_plural = "Страницы инфраструктуры"
