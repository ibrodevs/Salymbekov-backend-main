from django.db import models
import uuid
from django_ckeditor_5.fields import CKEditor5Field


class PageContent(models.Model):
    """
    Editable content for frontend pages/sections.
    Put repeatable blocks, links, gallery items, video IDs, etc. into data.
    """

    slug = models.SlugField("Slug", max_length=160, unique=True)
    path = models.CharField("Frontend path", max_length=255, unique=True, blank=True, null=True)

    title_ru = models.CharField("Title (RU)", max_length=255, blank=True)
    title_en = models.CharField("Title (EN)", max_length=255, blank=True)
    title_kg = models.CharField("Title (KG)", max_length=255, blank=True)

    subtitle_ru = models.TextField("Subtitle (RU)", blank=True)
    subtitle_en = models.TextField("Subtitle (EN)", blank=True)
    subtitle_kg = models.TextField("Subtitle (KG)", blank=True)

    body_ru = CKEditor5Field("Body (RU)", blank=True, config_name="extends")
    body_en = CKEditor5Field("Body (EN)", blank=True, config_name="extends")
    body_kg = CKEditor5Field("Body (KG)", blank=True, config_name="extends")

    data = models.JSONField("Structured data", default=dict, blank=True)
    is_active = models.BooleanField("Active", default=True)

    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        ordering = ["slug"]
        verbose_name = "Page content"
        verbose_name_plural = "Page contents"

    def __str__(self):
        return self.slug


class PageMedia(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"

    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
        (FILE, "File"),
    ]

    page = models.ForeignKey(PageContent, related_name="media", on_delete=models.CASCADE)
    key = models.SlugField("Key", max_length=120, blank=True)
    title = models.CharField("Title", max_length=255, blank=True)
    media_type = models.CharField("Type", max_length=20, choices=MEDIA_TYPE_CHOICES, default=IMAGE)
    file = models.FileField("File", upload_to="pages/", blank=True, null=True)
    external_url = models.URLField("External URL", blank=True)
    order = models.PositiveIntegerField("Order", default=0)
    is_active = models.BooleanField("Active", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Page media"
        verbose_name_plural = "Page media"

    def __str__(self):
        return self.title or self.key or f"{self.page.slug} media"


class DevelopmentCouncilMember(models.Model):
    """
    Член Совета по развитию
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name_ru = models.CharField("ФИО (рус)", max_length=255, blank=True)
    full_name_en = models.CharField("Full Name (eng)", max_length=255, blank=True)
    full_name_kg = models.CharField("ФИО (кр)", max_length=255, blank=True)

    role_ru = models.CharField("Должность (рус)", max_length=255, blank=True)
    role_en = models.CharField("Role (eng)", max_length=255, blank=True)
    role_kg = models.CharField("Кызмат орду (кр)", max_length=255, blank=True)

    description_ru = CKEditor5Field("Описание (рус)", blank=True, config_name='default')
    description_en = CKEditor5Field("Description (eng)", blank=True, config_name='default')
    description_kg = CKEditor5Field("Суроттомо (кр)", blank=True, config_name='default')

    photo = models.ImageField("Фото", upload_to='council/', blank=True, null=True)

    is_council_member = models.BooleanField("Состав совета", default=False)
    is_active = models.BooleanField("Активен", default=True)

    order = models.PositiveIntegerField("Порядок сортировки", default=0)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Член Совета по развитию"
        verbose_name_plural = "Члены Совета по развитию"

    def __str__(self):
        return self.full_name_ru or self.full_name_en or self.full_name_kg or "Без имени"


class ScientificTechnicalCouncilMember(models.Model):
    """
    Член Научно-Технического Совета
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name_ru = models.CharField("ФИО (рус)", max_length=255, blank=True)
    full_name_en = models.CharField("Full Name (eng)", max_length=255, blank=True)
    full_name_kg = models.CharField("ФИО (кр)", max_length=255, blank=True)

    role_ru = models.CharField("Должность (рус)", max_length=255, blank=True)
    role_en = models.CharField("Role (eng)", max_length=255, blank=True)
    role_kg = models.CharField("Кызмат орду(кр)", max_length=255, blank=True)

    is_head = models.BooleanField("Руководство совета", default=False)
    is_active = models.BooleanField("Активен", default=True)

    order = models.PositiveIntegerField("Порядок сортировки", default=0)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Член Научно-Технического Совета"
        verbose_name_plural = "Члены Научно-Технического Совета"

    def __str__(self):
        return self.full_name_ru or self.full_name_en or self.full_name_kg or "Без имени"
