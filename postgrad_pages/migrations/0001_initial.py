from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = [('cms_pages', '0009_review_licenses_brandbook_provenance')]
    operations = [
        migrations.CreateModel(
            name='PostgradPage', fields=[],
            options={'verbose_name': 'Страница Postgraduate', 'verbose_name_plural': 'Страницы Postgraduate', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('cms_pages.page',),
        ),
    ]
