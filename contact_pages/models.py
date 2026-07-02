from django.db import models

from cms_pages.models import Page
from about_pages.utils import about_scope_query


class ContactPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(about_scope_query("contacts"))


class ContactPage(Page):
    objects = ContactPageManager()

    class Meta:
        proxy = True
        app_label = "contact_pages"
        verbose_name = "Страница контактов"
        verbose_name_plural = "Страницы контактов"
