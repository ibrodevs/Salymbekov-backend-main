from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = [('cms_pages', '0009_review_licenses_brandbook_provenance')]
    operations = [
        migrations.CreateModel(
            name='ClinicalPage', fields=[],
            options={'verbose_name': 'Страница клинической базы', 'verbose_name_plural': 'Страницы клинической базы', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('cms_pages.page',),
        ),
    ]
