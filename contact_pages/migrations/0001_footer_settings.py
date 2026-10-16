from django.db import migrations, models
import django.db.models.deletion


def seed_footer(apps, schema_editor):
    FooterSettings = apps.get_model("contact_pages", "FooterSettings")
    FooterLink = apps.get_model("contact_pages", "FooterLink")

    footer, _ = FooterSettings.objects.get_or_create(
        key="main",
        defaults={
            "brand_ru": "SALYMBEKOV UNIVERSITY",
            "brand_en": "SALYMBEKOV UNIVERSITY",
            "brand_kg": "SALYMBEKOV UNIVERSITY",
            "description_ru": "Современный университет, объединяющий качественное образование, науку и международное сотрудничество.",
            "description_en": "A modern university combining quality education, science, and international cooperation.",
            "description_kg": "Сапаттуу билим берүүнү, илимди жана эл аралык кызматташууну бириктирген заманбап университет.",
            "address_ru": "Кыргызская Республика, г. Бишкек, ул. Фучика, 3",
            "address_en": "3 Fuchik St., Bishkek, Kyrgyz Republic",
            "address_kg": "Кыргыз Республикасы, Бишкек ш., Фучик көч., 3",
            "phone": "+996 (312) 65 85 38",
            "email": "info@salymbekov.com",
            "website": "https://salymbekov.com",
            "quick_links_title_ru": "Быстрые ссылки",
            "quick_links_title_en": "Quick links",
            "quick_links_title_kg": "Тез шилтемелер",
            "academic_title_ru": "Образовательные программы",
            "academic_title_en": "Academic programs",
            "academic_title_kg": "Билим берүү программалары",
            "social_title_ru": "Мы в социальных сетях",
            "social_title_en": "Follow us",
            "social_title_kg": "Биз социалдык тармактарда",
            "copyright_ru": "Все права защищены.",
            "copyright_en": "All rights reserved.",
            "copyright_kg": "Бардык укуктар корголгон.",
            "is_active": True,
        },
    )

    links = [
        ("quick", "О нас", "About us", "Биз жөнүндө", "/university/structure/university-main", "", 10),
        ("quick", "Наука", "Science", "Илим", "/science/labs", "", 20),
        ("quick", "Контакты", "Contacts", "Байланыш", "/contacts", "", 30),
        ("academic", "Американский институт технологий", "American Institute of Technology", "Америкалык технологиялар институту", "/education/ait/about", "", 10),
        ("academic", "Международный факультет медицины", "International Faculty of Medicine", "Эл аралык медицина факультети", "/education/mfm/about", "", 20),
        ("academic", "Международный колледж IT и бизнеса", "International College of IT and Business", "Эл аралык IT жана бизнес колледжи", "/university/structure/it-college", "", 30),
        ("social", "Facebook", "Facebook", "Facebook", "https://www.facebook.com/salymbekov.kg/", "facebook", 10),
        ("social", "Instagram", "Instagram", "Instagram", "https://www.instagram.com/salymbekovuniversity", "instagram", 20),
        ("social", "YouTube", "YouTube", "YouTube", "https://www.youtube.com/@salymbekovuniversity8213/", "youtube", 30),
    ]

    for section, ru, en, kg, url, icon, order in links:
        FooterLink.objects.get_or_create(
            footer=footer,
            section=section,
            url=url,
            defaults={
                "title_ru": ru,
                "title_en": en,
                "title_kg": kg,
                "icon": icon,
                "order": order,
                "is_active": True,
            },
        )


def unseed_footer(apps, schema_editor):
    FooterSettings = apps.get_model("contact_pages", "FooterSettings")
    FooterSettings.objects.filter(key="main").delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FooterSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(default="main", editable=False, max_length=32, unique=True)),
                ("brand_ru", models.CharField(default="SALYMBEKOV UNIVERSITY", max_length=255, verbose_name="Бренд (RU)")),
                ("brand_en", models.CharField(default="SALYMBEKOV UNIVERSITY", max_length=255, verbose_name="Brand (EN)")),
                ("brand_kg", models.CharField(default="SALYMBEKOV UNIVERSITY", max_length=255, verbose_name="Бренд (KG)")),
                ("description_ru", models.TextField(blank=True, verbose_name="Описание (RU)")),
                ("description_en", models.TextField(blank=True, verbose_name="Description (EN)")),
                ("description_kg", models.TextField(blank=True, verbose_name="Сүрөттөмө (KG)")),
                ("address_ru", models.CharField(blank=True, max_length=500, verbose_name="Адрес (RU)")),
                ("address_en", models.CharField(blank=True, max_length=500, verbose_name="Address (EN)")),
                ("address_kg", models.CharField(blank=True, max_length=500, verbose_name="Дарек (KG)")),
                ("phone", models.CharField(blank=True, max_length=100, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("website", models.URLField(blank=True, verbose_name="Сайт")),
                ("quick_links_title_ru", models.CharField(default="Быстрые ссылки", max_length=255, verbose_name="Быстрые ссылки (RU)")),
                ("quick_links_title_en", models.CharField(default="Quick links", max_length=255, verbose_name="Quick links (EN)")),
                ("quick_links_title_kg", models.CharField(default="Тез шилтемелер", max_length=255, verbose_name="Тез шилтемелер (KG)")),
                ("academic_title_ru", models.CharField(default="Образовательные программы", max_length=255, verbose_name="Образовательные программы (RU)")),
                ("academic_title_en", models.CharField(default="Academic programs", max_length=255, verbose_name="Academic programs (EN)")),
                ("academic_title_kg", models.CharField(default="Билим берүү программалары", max_length=255, verbose_name="Билим берүү программалары (KG)")),
                ("social_title_ru", models.CharField(default="Мы в социальных сетях", max_length=255, verbose_name="Социальные сети (RU)")),
                ("social_title_en", models.CharField(default="Follow us", max_length=255, verbose_name="Social networks (EN)")),
                ("social_title_kg", models.CharField(default="Биз социалдык тармактарда", max_length=255, verbose_name="Социалдык тармактар (KG)")),
                ("copyright_ru", models.CharField(blank=True, max_length=500, verbose_name="Copyright (RU)")),
                ("copyright_en", models.CharField(blank=True, max_length=500, verbose_name="Copyright (EN)")),
                ("copyright_kg", models.CharField(blank=True, max_length=500, verbose_name="Copyright (KG)")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
            ],
            options={
                "verbose_name": "Настройки footer",
                "verbose_name_plural": "Настройки footer",
            },
        ),
        migrations.CreateModel(
            name="FooterLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("section", models.CharField(choices=[("quick", "Быстрые ссылки"), ("academic", "Образовательные программы"), ("social", "Социальные сети")], max_length=16, verbose_name="Раздел")),
                ("title_ru", models.CharField(blank=True, max_length=255, verbose_name="Название (RU)")),
                ("title_en", models.CharField(blank=True, max_length=255, verbose_name="Title (EN)")),
                ("title_kg", models.CharField(blank=True, max_length=255, verbose_name="Аталышы (KG)")),
                ("url", models.CharField(max_length=500, verbose_name="URL")),
                ("icon", models.CharField(blank=True, help_text="Для соцсетей: facebook, instagram, youtube, linkedin. Для обычных ссылок можно оставить пустым.", max_length=32, verbose_name="Иконка")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
                ("footer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="links", to="contact_pages.footersettings")),
            ],
            options={
                "verbose_name": "Ссылка footer",
                "verbose_name_plural": "Ссылки footer",
                "ordering": ["section", "order", "id"],
            },
        ),
        migrations.RunPython(seed_footer, unseed_footer),
    ]
