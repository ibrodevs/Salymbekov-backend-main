from django.db import migrations


LEGACY_FRONTEND_PATHS = {
    "/",
    "/news",
    "/news/NewsHome",
    "/press/news",
}

TITLE_OVERRIDES = {
    "/about": "About",
    "/contact": "Contact",
    "/contacts": "Contacts",
    "/services": "Services",
    "/vacancies": "Vacancies",
    "/founderMessege": "Founder Message",
    "/MaterialBaseGallery": "Material Base Gallery",
    "/university/mission": "University Mission",
    "/university/structure": "University Structure",
    "/university/management": "University Management",
    "/university/normative-docs": "Normative Documents",
    "/university/councils/academic-council": "Academic Council",
    "/university/councils/development-council": "Development Council",
    "/university/councils/scientific-council": "Scientific Council",
    "/education/ait": "AIT",
    "/education/mfm": "Medical Faculty",
    "/education/it-college": "IT College",
    "/education/postgrad": "Postgraduate Education",
    "/education/center": "Education Center",
    "/clinical/doc-clinic": "DOC Clinic",
    "/clinical/doc-hospital": "DOC Hospital",
    "/clinical/simulation-center": "Simulation Center",
    "/clinical/startups": "Startups",
    "/science/management": "Science Management",
    "/science/department": "Science Department",
    "/science/events": "Science Events",
    "/science/projects": "Science Projects",
    "/science/publications": "Science Publications",
    "/science/labs": "Science Labs",
    "/cooperation/international-partners": "International Partners",
    "/cooperation/local-partners": "Local Partners",
    "/infrastructure/locations": "Locations",
    "/infrastructure/partners": "Infrastructure Partners",
}


def humanize_path(path):
    title = TITLE_OVERRIDES.get(path)
    if title:
        return title

    last_segment = path.strip("/").split("/")[-1]
    return last_segment.replace("-", " ").replace("_", " ").title()


def mark_cms_first_pages(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")

    pages = PageContent.objects.exclude(path__isnull=True).exclude(path="").exclude(path__in=LEGACY_FRONTEND_PATHS)

    for page in pages:
        data = dict(page.data or {})
        data.setdefault("force_backend_render", True)
        data.setdefault(
            "empty_message",
            "Контент этой страницы теперь управляется из админки. Заполните заголовок, текст, блоки и медиа в Page contents.",
        )

        title = humanize_path(page.path)
        updates = {"data": data}

        if not page.title_ru:
            updates["title_ru"] = title
        if not page.title_en:
            updates["title_en"] = title
        if not page.title_kg:
            updates["title_kg"] = title

        PageContent.objects.filter(pk=page.pk).update(**updates)


def unmark_cms_first_pages(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")

    pages = PageContent.objects.exclude(path__isnull=True).exclude(path="").exclude(path__in=LEGACY_FRONTEND_PATHS)

    for page in pages:
        data = dict(page.data or {})
        data.pop("force_backend_render", None)
        if data.get("empty_message") == "Контент этой страницы теперь управляется из админки. Заполните заголовок, текст, блоки и медиа в Page contents.":
            data.pop("empty_message", None)
        PageContent.objects.filter(pk=page.pk).update(data=data)


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0008_seed_frontend_page_paths"),
    ]

    operations = [
        migrations.RunPython(mark_cms_first_pages, unmark_cms_first_pages),
    ]
