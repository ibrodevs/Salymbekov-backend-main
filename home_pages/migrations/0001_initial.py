from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('banners', '0001_initial'),
        ('cms_pages', '0009_review_licenses_brandbook_provenance'),
        ('partners', '0003_remove_placeholder_partner'),
    ]
    operations = [
        migrations.CreateModel(
            name='HomeBanner', fields=[],
            options={'verbose_name': 'Главная: баннер', 'verbose_name_plural': 'Главная: баннеры hero', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('banners.banner',),
        ),
        migrations.CreateModel(
            name='HomeFounderPage', fields=[],
            options={'verbose_name': 'Главная: блок учредителя', 'verbose_name_plural': 'Главная: блок учредителя', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('cms_pages.page',),
        ),
        migrations.CreateModel(
            name='HomeGalleryPage', fields=[],
            options={'verbose_name': 'Главная: галерея', 'verbose_name_plural': 'Главная: галерея', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('cms_pages.page',),
        ),
        migrations.CreateModel(
            name='HomePage', fields=[],
            options={'verbose_name': 'Главная страница', 'verbose_name_plural': 'Главная страница', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('cms_pages.page',),
        ),
        migrations.CreateModel(
            name='HomePartner', fields=[],
            options={'verbose_name': 'Главная: партнер', 'verbose_name_plural': 'Главная: партнеры', 'proxy': True, 'indexes': [], 'constraints': []},
            bases=('partners.partner',),
        ),
    ]
