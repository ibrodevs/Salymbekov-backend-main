from django.db import migrations


DEFAULT_PARTNERS = [
    {
        "name_ru": "Salymbekov University",
        "name_en": "Salymbekov University",
        "name_kg": "Salymbekov University",
        "description_ru": "<p>Стратегический образовательный партнер.</p>",
        "description_en": "<p>Strategic educational partner.</p>",
        "description_kg": "<p>Стратегиялык билим берүү өнөктөшү.</p>",
        "logo": "partners/logos/su-logo.png",
    },
    {
        "name_ru": "Asan Medical Center",
        "name_en": "Asan Medical Center",
        "name_kg": "Asan Medical Center",
        "description_ru": "<p>Международный клинический партнер.</p>",
        "description_en": "<p>International clinical partner.</p>",
        "description_kg": "<p>Эл аралык клиникалык өнөктөш.</p>",
    },
    {
        "name_ru": "Sarvodaya Hospital",
        "name_en": "Sarvodaya Hospital",
        "name_kg": "Sarvodaya Hospital",
        "description_ru": "<p>Партнер по медицинской практике и стажировкам.</p>",
        "description_en": "<p>Partner for medical practice and internships.</p>",
        "description_kg": "<p>Медициналык практика жана стажировка боюнча өнөктөш.</p>",
    },
    {
        "name_ru": "Pai Chai University",
        "name_en": "Pai Chai University",
        "name_kg": "Pai Chai University",
        "description_ru": "<p>Партнер по академическому сотрудничеству.</p>",
        "description_en": "<p>Academic cooperation partner.</p>",
        "description_kg": "<p>Академиялык кызматташтык боюнча өнөктөш.</p>",
    },
    {
        "name_ru": "Douzone Bizon",
        "name_en": "Douzone Bizon",
        "name_kg": "Douzone Bizon",
        "description_ru": "<p>IT-партнер для международных стажировок.</p>",
        "description_en": "<p>IT partner for international internships.</p>",
        "description_kg": "<p>Эл аралык стажировкалар боюнча IT өнөктөш.</p>",
    },
    {
        "name_ru": "Peter the Great St. Petersburg Polytechnic University",
        "name_en": "Peter the Great St. Petersburg Polytechnic University",
        "name_kg": "Peter the Great St. Petersburg Polytechnic University",
        "description_ru": "<p>Партнер по международным образовательным программам.</p>",
        "description_en": "<p>Partner for international education programs.</p>",
        "description_kg": "<p>Эл аралык билим берүү программалары боюнча өнөктөш.</p>",
    },
    {
        "name_ru": "SK Career Builder LLC",
        "name_en": "SK Career Builder LLC",
        "name_kg": "SK Career Builder LLC",
        "description_ru": "<p>Партнер по привлечению и сопровождению студентов.</p>",
        "description_en": "<p>Partner for student recruitment and support.</p>",
        "description_kg": "<p>Студенттерди тартуу жана коштоо боюнча өнөктөш.</p>",
    },
    {
        "name_ru": "Korean Center",
        "name_en": "Korean Center",
        "name_kg": "Korean Center",
        "description_ru": "<p>Партнер по международным культурным и образовательным проектам.</p>",
        "description_en": "<p>Partner for international cultural and educational projects.</p>",
        "description_kg": "<p>Эл аралык маданий жана билим берүү долбоорлору боюнча өнөктөш.</p>",
    },
]


def seed_default_partners(apps, schema_editor):
    Partner = apps.get_model("partners", "Partner")

    for item in DEFAULT_PARTNERS:
        defaults = {key: value for key, value in item.items() if key != "name_ru"}
        Partner.objects.update_or_create(name_ru=item["name_ru"], defaults=defaults)


def remove_default_partners(apps, schema_editor):
    Partner = apps.get_model("partners", "Partner")
    Partner.objects.filter(name_ru__in=[item["name_ru"] for item in DEFAULT_PARTNERS[1:]]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_partners, remove_default_partners),
    ]
