"""Canonical CMS routes used by the public frontend.

Keep this inventory in the backend so production bootstrap/audit does not depend
on the frontend repository being present on the Heroku filesystem.
"""

CMS_PAGE_PATHS = (
    "/",
    "/about",
    "/services",
    "/contact",
    "/contacts",
    "/vacancies",
    "/founderMessege",
    "/MaterialBaseGallery",
    "/university/mission",
    "/university/structure",
    "/university/structure/university-main",
    "/university/structure/international-faculty",
    "/university/structure/it-college",
    "/university/management",
    "/university/management/founder",
    "/university/management/rectorate",
    "/university/management/public-councils",
    "/university/normative-docs",
    "/university/normative-docs/kr-acts",
    "/university/normative-docs/internal-acts",
    "/university/normative-docs/licenses",
    "/university/normative-docs/logo",
    "/university/councils/academic-council",
    "/university/councils/admissions-committee",
    "/university/councils/bioethics-committee",
    "/university/councils/commission-support",
    "/university/councils/council-scients",
    "/university/councils/development-council",
    "/university/councils/editorial-board",
    "/university/councils/educational-council",
    "/university/councils/employers-council",
    "/university/councils/scientific-council",
    "/university/councils/student-councils",
    "/university/councils/technical-council",
    "/university/councils/parents-council",
    "/university/quality-management-system/quality-monitoring",
    "/university/quality-management-system/quality-policy",
    "/education/ait",
    "/education/ait/about",
    "/education/ait/leadership",
    "/education/ait/disciplines",
    "/education/ait/teachers",
    "/education/ait/contacts",
    "/education/mfm",
    "/education/mfm/about",
    "/education/mfm/dekanat/dean",
    "/education/mfm/dekanat/curriculum",
    "/education/mfm/dekanat/departments",
    "/education/mfm/programs/five-years",
    "/education/mfm/programs/six-years",
    "/education/it-college",
    "/education/it-college/departments/general",
    "/education/it-college/departments/information",
    "/education/it-college/specialties/diplom-computational-sciences",
    "/education/it-college/specialties/diplom-mobile-computing",
    "/education/it-college/specialties/diplom-multimedia-applications",
    "/education/it-college/director",
    "/education/it-college/double-diploma",
    "/education/it-college/pedagogical-council",
    "/education/postgrad",
    "/education/postgrad/internship",
    "/education/postgrad/phd",
    "/education/postgrad/postgraduate",
    "/education/postgrad/residency",
    "/education/center",
    "/education/center/about",
    "/clinical/doc-clinic",
    "/clinical/doc-hospital",
    "/clinical/simulation-center",
    "/clinical/startups",
    "/science/management",
    "/science/management/scientific-council",
    "/science/management/scientific-technical-council",
    "/science/management/bioethics",
    "/science/management/young-scientists",
    "/science/management/department",
    "/science/department",
    "/science/events",
    "/science/events/conferences",
    "/science/publications",
    "/science/publications/journal",
    "/science/scholarships",
    "/science/labs",
    "/science/labs/anatomy",
    "/science/labs/biochemistry",
    "/science/labs/biology",
    "/science/labs/interactive",
    "/science/labs/computer",
    "/science/labs/study",
    "/science/projects",
    "/cooperation/international-partners",
    "/cooperation/local-partners",
    "/infrastructure/locations",
    "/infrastructure/partners",
)


def humanize_path(path_value):
    if path_value == "/":
        return "Главная"

    parts = [part for part in path_value.strip("/").split("/") if part]
    if not parts:
        return "Страница"

    return " / ".join(part.replace("-", " ").replace("_", " ").title() for part in parts)


def navigation_group_for(path_value):
    clean = path_value.strip("/")
    return clean.split("/", 1)[0] if clean else "main"
