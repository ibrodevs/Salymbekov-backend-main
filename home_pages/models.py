from django.db import models

from banners.models import Banner
from cms_pages.models import Page
from partners.models import Partner


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


class HomeFounderPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(path="/founderMessege")


class HomeFounderPage(Page):
    objects = HomeFounderPageManager()

    class Meta:
        proxy = True
        app_label = "home_pages"
        verbose_name = "Главная: блок учредителя"
        verbose_name_plural = "Главная: блок учредителя"


class HomeGalleryPageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(path="/MaterialBaseGallery")


class HomeGalleryPage(Page):
    objects = HomeGalleryPageManager()

    class Meta:
        proxy = True
        app_label = "home_pages"
        verbose_name = "Главная: галерея"
        verbose_name_plural = "Главная: галерея"


class HomeBanner(Banner):
    class Meta:
        proxy = True
        app_label = "home_pages"
        verbose_name = "Главная: баннер"
        verbose_name_plural = "Главная: баннеры hero"


class HomePartner(Partner):
    class Meta:
        proxy = True
        app_label = "home_pages"
        verbose_name = "Главная: партнер"
        verbose_name_plural = "Главная: партнеры"
