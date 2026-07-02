from django.db import models

from cms_pages.models import Page
from .utils import about_scope_query


class AboutPageQuerySet(models.QuerySet):
    def for_admin(self):
        return self.filter(
            about_scope_query(
                "main",
                "university",
                "clinical",
                "infrastructure",
                "cooperation",
                "contacts",
            )
        )


class AboutPageManager(models.Manager):
    def get_queryset(self):
        return AboutPageQuerySet(self.model, using=self._db).for_admin()


class AboutPage(Page):
    objects = AboutPageManager()

    class Meta:
        proxy = True
        app_label = "about_pages"
        verbose_name = "Страница раздела О нас"
        verbose_name_plural = "Страницы раздела О нас"
