from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("presscentre", "0013_remove_news_is_banner"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="external_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="ID новости в старом WordPress сайте",
                max_length=64,
                verbose_name="Внешний ID",
            ),
        ),
        migrations.AddField(
            model_name="news",
            name="source_url",
            field=models.URLField(
                blank=True,
                help_text="Ссылка на оригинальную новость",
                max_length=500,
                verbose_name="Источник",
            ),
        ),
        migrations.AddIndex(
            model_name="news",
            index=models.Index(fields=["external_id"], name="news_external_id_idx"),
        ),
    ]
