from django.db import models

from cms_pages.models import Page


class HomePageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(path="/")


class HomePage(Page):
    objects = HomePageManager()

    class Meta:
        proxy = True
        app_label = "home_pages"
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

