from django.db import migrations, models


def preserve_explicit_galleries(apps, schema_editor):
    Page = apps.get_model('cms_pages', 'Page')
    for page in Page.objects.all().iterator():
        if (page.data or {}).get('show_media_gallery') is True or page.path == '/MaterialBaseGallery':
            Page.objects.filter(pk=page.pk).update(show_media_gallery=True)


class Migration(migrations.Migration):
    dependencies = [('cms_pages', '0009_review_licenses_brandbook_provenance')]
    operations = [
        migrations.AddField(model_name="pagelink", name="is_active", field=models.BooleanField(default=True, verbose_name="Активна")),
        migrations.AddField(model_name='page', name='show_media_gallery', field=models.BooleanField(default=False, verbose_name='Показывать отдельную галерею')),
        migrations.RunPython(preserve_explicit_galleries, migrations.RunPython.noop),
    ]
