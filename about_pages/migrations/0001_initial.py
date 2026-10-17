from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('cms_pages', '0009_review_licenses_brandbook_provenance'),
    ]
    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[],
            options={
                'verbose_name': 'Страница раздела О нас',
                'verbose_name_plural': 'Страницы раздела О нас',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('cms_pages.page',),
        ),
    ]
