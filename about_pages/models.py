from django.db import models

from cms_pages.models import Page


class AboutPageQuerySet(models.QuerySet):
    def for_admin(self):
        return self.filter(
            models.Q(path="/about")
            | models.Q(path__startswith="/university/")
            | models.Q(path__startswith="/contacts")
            | models.Q(path__startswith="/contact")
            | models.Q(path__startswith="/cooperation/")
            | models.Q(path__startswith="/infrastructure/")
            | models.Q(path__startswith="/clinical/")
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

