from django.db import models
import uuid
from django_ckeditor_5.fields import CKEditor5Field


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