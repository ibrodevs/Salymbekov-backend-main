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


class FooterSettings(models.Model):
    key = models.CharField(max_length=32, unique=True, default="main", editable=False)

    brand_ru = models.CharField("Бренд (RU)", max_length=255, default="SALYMBEKOV UNIVERSITY")
    brand_en = models.CharField("Brand (EN)", max_length=255, default="SALYMBEKOV UNIVERSITY")
    brand_kg = models.CharField("Бренд (KG)", max_length=255, default="SALYMBEKOV UNIVERSITY")

    description_ru = models.TextField("Описание (RU)", blank=True)
    description_en = models.TextField("Description (EN)", blank=True)
    description_kg = models.TextField("Сүрөттөмө (KG)", blank=True)

    address_ru = models.CharField("Адрес (RU)", max_length=500, blank=True)
    address_en = models.CharField("Address (EN)", max_length=500, blank=True)
    address_kg = models.CharField("Дарек (KG)", max_length=500, blank=True)

    phone = models.CharField("Телефон", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)
    website = models.URLField("Сайт", blank=True)

    quick_links_title_ru = models.CharField("Быстрые ссылки (RU)", max_length=255, default="Быстрые ссылки")
    quick_links_title_en = models.CharField("Quick links (EN)", max_length=255, default="Quick links")
    quick_links_title_kg = models.CharField("Тез шилтемелер (KG)", max_length=255, default="Тез шилтемелер")

    academic_title_ru = models.CharField("Образовательные программы (RU)", max_length=255, default="Образовательные программы")
    academic_title_en = models.CharField("Academic programs (EN)", max_length=255, default="Academic programs")
    academic_title_kg = models.CharField("Билим берүү программалары (KG)", max_length=255, default="Билим берүү программалары")

    social_title_ru = models.CharField("Социальные сети (RU)", max_length=255, default="Мы в социальных сетях")
    social_title_en = models.CharField("Social networks (EN)", max_length=255, default="Follow us")
    social_title_kg = models.CharField("Социалдык тармактар (KG)", max_length=255, default="Биз социалдык тармактарда")

    copyright_ru = models.CharField("Copyright (RU)", max_length=500, blank=True)
    copyright_en = models.CharField("Copyright (EN)", max_length=500, blank=True)
    copyright_kg = models.CharField("Copyright (KG)", max_length=500, blank=True)

    is_active = models.BooleanField("Активен", default=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Настройки footer"
        verbose_name_plural = "Настройки footer"

    def __str__(self):
        return "Footer сайта"


class FooterLink(models.Model):
    SECTION_QUICK = "quick"
    SECTION_ACADEMIC = "academic"
    SECTION_SOCIAL = "social"
    SECTION_CHOICES = (
        (SECTION_QUICK, "Быстрые ссылки"),
        (SECTION_ACADEMIC, "Образовательные программы"),
        (SECTION_SOCIAL, "Социальные сети"),
    )

    footer = models.ForeignKey(FooterSettings, on_delete=models.CASCADE, related_name="links")
    section = models.CharField("Раздел", max_length=16, choices=SECTION_CHOICES)
    title_ru = models.CharField("Название (RU)", max_length=255, blank=True)
    title_en = models.CharField("Title (EN)", max_length=255, blank=True)
    title_kg = models.CharField("Аталышы (KG)", max_length=255, blank=True)
    url = models.CharField("URL", max_length=500)
    icon = models.CharField(
        "Иконка",
        max_length=32,
        blank=True,
        help_text="Для соцсетей: facebook, instagram, youtube, linkedin. Для обычных ссылок можно оставить пустым.",
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["section", "order", "id"]
        verbose_name = "Ссылка footer"
        verbose_name_plural = "Ссылки footer"

    def __str__(self):
        return self.title_ru or self.title_en or self.title_kg or self.url
