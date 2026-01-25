from django.db import models

# Create your models here.
class AcademicCouncil(models.Model):
    name_ru = models.CharField(max_length=255, verbose_name='ФИО на русском')
    name_en = models.CharField(max_length=255, verbose_name='ФИО на английском')
    name_kg = models.CharField(max_length=255, verbose_name='ФИО на кыргызском')

    role = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='acadmic_council_photos/')

    def __str__(self):
        return self.name_ru

    def get_name(self, lang='ru'):
        return getattr(self, f'name_{lang}', self.name_ru)
    
    class Meta:
        verbose_name = 'Член академического совета'
        verbose_name_plural = 'Члены академического совета'

