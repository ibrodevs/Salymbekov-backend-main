from django.db import models


PROGRAM_PATH_GROUPS = {
    "mfm": models.Q(path__startswith="/education/mfm"),
    "ait": models.Q(path__startswith="/education/ait"),
    "it_college": models.Q(path__startswith="/education/it-college"),
    "postgrad": models.Q(path__startswith="/education/postgrad"),
    "center": models.Q(path__startswith="/education/center"),
}


PROGRAM_FAMILY_LABELS = {
    "mfm": "MFM",
    "ait": "AIT",
    "it_college": "IT College",
    "postgrad": "Postgraduate",
    "center": "Center",
}


def program_scope_query(*keys):
    query = models.Q()
    for key in keys:
        query |= PROGRAM_PATH_GROUPS[key]
    return query


def program_family_from_path(path):
    if path.startswith("/education/mfm/") or path == "/education/mfm":
        return PROGRAM_FAMILY_LABELS["mfm"]
    if path.startswith("/education/ait/") or path == "/education/ait":
        return PROGRAM_FAMILY_LABELS["ait"]
    if path.startswith("/education/it-college/") or path == "/education/it-college":
        return PROGRAM_FAMILY_LABELS["it_college"]
    if path.startswith("/education/postgrad/") or path == "/education/postgrad":
        return PROGRAM_FAMILY_LABELS["postgrad"]
    if path.startswith("/education/center/") or path == "/education/center":
        return PROGRAM_FAMILY_LABELS["center"]
    return "Other"


def program_level_from_path(path):
    if "/programs/" in path:
        return "Программа"
    if "/specialties/" in path:
        return "Специальность"
    if "/departments/" in path:
        return "Подразделение"
    if path.endswith("/about"):
        return "О программе"
    if path.endswith("/contacts"):
        return "Контакты"
    if path.endswith("/director") or path.endswith("/dean"):
        return "Руководство"
    return "Общая страница"
