from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Partner(models.Model):
    logo = models.ImageField(upload_to="partners/logos/", verbose_name="Логотип", null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name="Название (EN)")
    name_ru = models.CharField(max_length=255, verbose_name="Название (RU)")
    name_kg = models.CharField(max_length=255, verbose_name="Название (KG)")
    description_ru = CKEditor5Field(
        "Description (RU)", config_name="extends", null=True, blank=True
    )
    description_en = CKEditor5Field(
        "Description (EN)", config_name="extends", null=True, blank=True
    )
    description_kg = CKEditor5Field(
        "Description (KG)", config_name="extends", null=True, blank=True
    )

    coord1 = models.CharField(max_length=55, verbose_name='координаты ширины(LAT)', null=True, blank=True)
    coord2 = models.CharField(max_length=55, verbose_name='координаты долготы(LMG)', null=True, blank=True)

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ["id"]   
    def __str__(self):
        return self.get_name()
    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)
    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)



