from django.db import migrations


def remove_placeholder_partner(apps, schema_editor):
    Partner = apps.get_model("partners", "Partner")
    Partner.objects.filter(name_ru="name in ru", name_en="name in en", name_kg="name in kg").delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0002_seed_default_partners"),
    ]

    operations = [
        migrations.RunPython(remove_placeholder_partner, noop),
    ]
