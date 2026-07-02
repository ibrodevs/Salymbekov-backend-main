from django.db import migrations


FRONTEND_PATHS = [
    "/",
    "/about",
    "/clinical/doc-clinic",
    "/clinical/doc-hospital",
    "/clinical/simulation-center",
    "/clinical/startups",
    "/contact",
    "/contacts",
    "/cooperation/international-partners",
    "/cooperation/local-partners",
    "/education/ait",
    "/education/ait/about",
    "/education/ait/contacts",
    "/education/ait/disciplines",
    "/education/ait/leadership",
    "/education/ait/teachers",
    "/education/center",
    "/education/center/about",
    "/education/it-college",
    "/education/it-college/departments/general",
    "/education/it-college/departments/information",
    "/education/it-college/director",
    "/education/it-college/double-diploma",
    "/education/it-college/pedagogical-council",
    "/education/it-college/specialties/diplom-computational-sciences",
    "/education/it-college/specialties/diplom-mobile-computing",
    "/education/it-college/specialties/diplom-multimedia-applications",
    "/education/mfm",
    "/education/mfm/about",
    "/education/mfm/dekanat/curriculum",
    "/education/mfm/dekanat/dean",
    "/education/mfm/dekanat/departments",
    "/education/mfm/programs/five-years",
    "/education/mfm/programs/six-years",
    "/education/postgrad",
    "/education/postgrad/internship",
    "/education/postgrad/phd",
    "/education/postgrad/postgraduate",
    "/education/postgrad/residency",
    "/founderMessege",
    "/infrastructure/locations",
    "/infrastructure/partners",
    "/MaterialBaseGallery",
    "/news",
    "/news/NewsHome",
    "/press/news",
    "/science/department",
    "/science/events",
    "/science/events/conferences",
    "/science/labs",
    "/science/labs/anatomy",
    "/science/labs/biochemistry",
    "/science/labs/biology",
    "/science/labs/computer",
    "/science/labs/interactive",
    "/science/labs/study",
    "/science/management",
    "/science/management/bioethics",
    "/science/management/department",
    "/science/management/scientific-council",
    "/science/management/scientific-technical-council",
    "/science/management/young-scientists",
    "/science/projects",
    "/science/publications",
    "/science/publications/journal",
    "/science/scholarships",
    "/services",
    "/university/councils/academic-council",
    "/university/councils/admissions-committee",
    "/university/councils/bioethics-committee",
    "/university/councils/commission-support",
    "/university/councils/council-scients",
    "/university/councils/development-council",
    "/university/councils/editorial-board",
    "/university/councils/educational-council",
    "/university/councils/employers-council",
    "/university/councils/parents-council",
    "/university/councils/scientific-council",
    "/university/councils/student-councils",
    "/university/councils/technical-council",
    "/university/management",
    "/university/management/founder",
    "/university/management/public-councils",
    "/university/management/rectorate",
    "/university/mission",
    "/university/normative-docs",
    "/university/normative-docs/internal-acts",
    "/university/normative-docs/kr-acts",
    "/university/quality-management-system/quality-monitoring",
    "/university/quality-management-system/quality-policy",
    "/university/structure",
    "/university/structure/international-faculty",
    "/university/structure/it-college",
    "/university/structure/university-main",
    "/vacancies",
]


def make_slug(path):
    if path == "/":
        return "home"

    slug = path.strip("/").lower()
    for char in ["/", "_", "."]:
        slug = slug.replace(char, "-")

    slug = "".join(char for char in slug if char.isalnum() or char == "-")
    while "--" in slug:
        slug = slug.replace("--", "-")

    return slug.strip("-")[:160]


def seed_frontend_paths(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")

    for path in FRONTEND_PATHS:
        slug = make_slug(path)
        obj = PageContent.objects.filter(path=path).first()

        if obj:
            continue

        if PageContent.objects.filter(slug=slug).exists():
            slug = f"page-{slug}"[:160]

        PageContent.objects.create(
            slug=slug,
            path=path,
            data={},
            is_active=True,
        )


def remove_frontend_paths(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")
    PageContent.objects.filter(path__in=FRONTEND_PATHS, title_ru="", title_en="", title_kg="", body_ru="", body_en="", body_kg="").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0007_pagecontent_path"),
    ]

    operations = [
        migrations.RunPython(seed_frontend_paths, remove_frontend_paths),
    ]
