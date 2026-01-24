from django.db import models

# Create your models here.
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return f'Banner {self.id}'
    
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'