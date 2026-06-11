from django.db import migrations


def seed_founder_message(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")
    PageContent.objects.update_or_create(
        slug="home-founder-message",
        defaults={
            "is_active": True,
            "data": {},
        },
    )


def remove_founder_message(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")
    PageContent.objects.filter(slug="home-founder-message").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0005_seed_home_page_content"),
    ]

    operations = [
        migrations.RunPython(seed_founder_message, remove_founder_message),
    ]
