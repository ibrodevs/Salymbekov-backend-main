from django.db import models


ABOUT_PATH_GROUPS = {
    "main": models.Q(path="/about"),
    "university": models.Q(path__startswith="/university/"),
    "clinical": models.Q(path__startswith="/clinical/"),
    "infrastructure": models.Q(path__startswith="/infrastructure/"),
    "cooperation": models.Q(path__startswith="/cooperation/"),
    "contacts": models.Q(path__startswith="/contact") | models.Q(path__startswith="/contacts"),
}


ABOUT_SECTION_LABELS = {
    "main": "Главная страница раздела",
    "university": "Университет",
    "clinical": "Клиническая база",
    "infrastructure": "Инфраструктура",
    "cooperation": "Сотрудничество",
    "contacts": "Контакты",
}


def about_scope_query(*keys):
    query = models.Q()
    for key in keys:
        query |= ABOUT_PATH_GROUPS[key]
    return query


def about_section_from_path(path):
    if path == "/about":
        return ABOUT_SECTION_LABELS["main"]
    if path.startswith("/university/"):
        return ABOUT_SECTION_LABELS["university"]
    if path.startswith("/clinical/"):
        return ABOUT_SECTION_LABELS["clinical"]
    if path.startswith("/infrastructure/"):
        return ABOUT_SECTION_LABELS["infrastructure"]
    if path.startswith("/cooperation/"):
        return ABOUT_SECTION_LABELS["cooperation"]
    if path.startswith("/contact") or path.startswith("/contacts"):
        return ABOUT_SECTION_LABELS["contacts"]
    return "Прочее"
