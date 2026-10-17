from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0006_ensure_uncovered_cms_pages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pagelink",
            name="url",
            field=models.CharField(
                "Ссылка",
                max_length=500,
                help_text="Можно указать внешний URL (https://...) или внутренний путь сайта (/education/...).",
            ),
        ),
    ]
