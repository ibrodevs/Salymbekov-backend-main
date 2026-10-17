from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cms_pages', '0009_review_licenses_brandbook_provenance'),
        ('contact_pages', '0001_footer_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPage',
            fields=[],
            options={
                'verbose_name': 'Страница контактов',
                'verbose_name_plural': 'Страницы контактов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('cms_pages.page',),
        ),
    ]
