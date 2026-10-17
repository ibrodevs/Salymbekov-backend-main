from django.db import migrations


DOUBLE_DIPLOMA = {
    "ru": {
        "title": "Программа двойного диплома",
        "subtitle": "Международные совместные образовательные программы",
        "body": """
<p>В материалах институциональной аккредитации Салымбеков Университета указано, что в 2019 году Университет заключил соглашение с образовательной организацией Южной Кореи для развития совместных IT-программ с возможностью продолжения обучения в Южной Корее и получения двойного диплома.</p>
<p>В тех же материалах отдельно указано соглашение с InHa Technical College (Инчхон, Южная Корея) о реализации совместных образовательных программ по техническим специальностям, включая программирование.</p>
<p>Конкретные действующие партнеры, сроки обучения и условия участия должны публиковаться администрацией Университета через CMS после актуальной проверки. Неподтвержденные сроки обучения и упоминание Lincoln University College удалены.</p>
""".strip(),
    },
    "en": {
        "title": "Double Degree Programme",
        "subtitle": "International joint education programmes",
        "body": """
<p>Salymbekov University's institutional accreditation materials state that in 2019 the University signed an agreement with an educational institution in South Korea to develop joint IT programmes with an opportunity to continue studies in South Korea and obtain a double degree.</p>
<p>The same materials also identify an agreement with InHa Technical College in Incheon, South Korea, for joint educational programmes in technical fields, including programming.</p>
<p>Current partners, study periods and participation conditions must be published by the University administration through the CMS after current verification. Unverified study-duration claims and the reference to Lincoln University College have been removed.</p>
""".strip(),
    },
    "kg": {
        "title": "Кош диплом программасы",
        "subtitle": "Эл аралык биргелешкен билим берүү программалары",
        "body": """
<p>Салымбеков Университетинин институционалдык аккредитация материалдарында 2019-жылы Түштүк Кореядагы билим берүү уюму менен биргелешкен IT-программаларды өнүктүрүү, Кореяда окууну улантуу жана кош диплом алуу мүмкүнчүлүгү боюнча келишим түзүлгөнү көрсөтүлгөн.</p>
<p>Ошол эле материалдарда Инчхон шаарындагы InHa Technical College менен программалоону кошо алганда техникалык адистиктер боюнча биргелешкен билим берүү программаларын ишке ашыруу тууралуу келишим өзүнчө көрсөтүлгөн.</p>
<p>Учурдагы өнөктөштөр, окуу мөөнөттөрү жана катышуу шарттары актуалдуу текшерүүдөн кийин Университеттин администрациясы тарабынан CMS аркылуу жарыяланышы керек. Тастыкталбаган окуу мөөнөттөрү жана Lincoln University College тууралуу маалымат алынып салынды.</p>
""".strip(),
    },
}

PUBLIC_COUNCILS = {
    "ru": {
        "title": "Общественные советы",
        "subtitle": "Советы и коллегиальные органы Салымбеков Университета",
        "body": """
<p>Эта страница служит навигационным разделом для советов и коллегиальных органов Университета. Подробный состав, задачи и документы каждого органа должны храниться на его отдельной CMS-странице.</p>
<p>Раздел не помечается как дословно восстановленный со старого сайта, потому что отдельный подтвержденный legacy-источник для этой сводной страницы не найден.</p>
""".strip(),
    },
    "en": {
        "title": "Public Councils",
        "subtitle": "Councils and collegial bodies of Salymbekov University",
        "body": """
<p>This page is a navigation hub for the University's councils and collegial bodies. The composition, functions and documents of each body should be maintained on its dedicated CMS page.</p>
<p>This index is not marked as a verbatim restoration from the former website because no confirmed legacy source for the combined page was found.</p>
""".strip(),
    },
    "kg": {
        "title": "Коомдук кеңештер",
        "subtitle": "Салымбеков Университетинин кеңештери жана коллегиалдык органдары",
        "body": """
<p>Бул барак Университеттин кеңештери жана коллегиалдык органдары үчүн навигациялык бөлүм болуп саналат. Ар бир органдын курамы, милдеттери жана документтери анын өзүнчө CMS-барагында жүргүзүлүшү керек.</p>
<p>Бул жыйнак барак эски сайттан сөзмө-сөз калыбына келтирилген деп белгиленбейт, анткени ага тиешелүү тастыкталган legacy-булак табылган жок.</p>
""".strip(),
    },
}

VACANCIES = {
    "ru": {
        "title": "Вакансии",
        "subtitle": "Карьера в Салымбеков Университете",
        "body": """
<p>Здесь должны публиковаться только актуальные вакансии Салымбеков Университета.</p>
<p>Исторические объявления со старого сайта не переносятся как действующие вакансии. До добавления актуальных объявлений администрацией Университета через CMS эта страница не содержит списка открытых позиций.</p>
<p>Общие контакты Университета: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
    "en": {
        "title": "Vacancies",
        "subtitle": "Careers at Salymbekov University",
        "body": """
<p>Only current Salymbekov University vacancies should be published here.</p>
<p>Historical job advertisements from the former website are not treated as active vacancies. Until the University administration adds current openings through the CMS, this page intentionally contains no list of open positions.</p>
<p>General University contacts: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
    "kg": {
        "title": "Бош орундар",
        "subtitle": "Салымбеков Университетиндеги карьера",
        "body": """
<p>Бул жерде Салымбеков Университетинин актуалдуу бош орундары гана жарыяланышы керек.</p>
<p>Эски сайттагы тарыхый жумуш жарыялары учурдагы вакансия катары көчүрүлбөйт. Университеттин администрациясы CMS аркылуу жаңы бош орундарды кошконго чейин бул баракта ачык кызматтардын тизмеси атайын көрсөтүлбөйт.</p>
<p>Университеттин жалпы байланыштары: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
}


def apply_page(page, payload, *, source_urls=None, status=None, note=None):
    for lang in ("ru", "en", "kg"):
        values = payload[lang]
        setattr(page, f"title_{lang}", values["title"])
        setattr(page, f"subtitle_{lang}", values["subtitle"])
        setattr(page, f"body_{lang}", values["body"])
        setattr(page, f"seo_title_{lang}", values["title"])
        setattr(page, f"seo_description_{lang}", values["subtitle"])

    data = dict(page.data or {})
    data["render_mode"] = "default"
    data.pop("verified_source_urls", None)
    data.pop("verified_legacy_source", None)
    if source_urls:
        data["verified_source_urls"] = source_urls
    if status:
        data["content_status"] = status
    data["source_reviewed_date"] = "2026-10-17"
    page.data = data
    page.force_backend_render = True
    page.is_published = True
    if note:
        page.internal_notes = note
    page.save()


def correct_unverified_content(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")

    page = Page.objects.filter(path="/education/it-college/double-diploma").first()
    if page:
        apply_page(
            page,
            DOUBLE_DIPLOMA,
            source_urls=["https://www.aaopo.kg/uploads/topics/16746194716331.pdf"],
            status="verified-historical-summary-needs-current-program-update",
            note="Исправлено после проверки источников: удалены неподтвержденные сроки обучения и Lincoln University College. Оставлены только сведения, подтвержденные материалами институциональной аккредитации.",
        )

    page = Page.objects.filter(path="/university/management/public-councils").first()
    if page:
        apply_page(
            page,
            PUBLIC_COUNCILS,
            status="cms-navigation-index-not-legacy-copy",
            note="Сводная страница не имеет найденного подтвержденного legacy-источника. Используется только как CMS-навигационный раздел; содержание отдельных советов хранится на их собственных страницах.",
        )

    page = Page.objects.filter(path="/vacancies").first()
    if page:
        apply_page(
            page,
            VACANCIES,
            status="requires-current-admin-vacancies",
            note="Исторические вакансии не публикуются как действующие. Администратор должен добавлять только актуальные вакансии через CMS.",
        )

    # Quality monitoring and simulation-center content from migration 0005 remain valid:
    # quality monitoring is backed by the former official page, and simulation-center
    # by the University's official medical education programme. Their provenance is retained.


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0007_allow_internal_page_links"),
    ]

    operations = [
        migrations.RunPython(correct_unverified_content, migrations.RunPython.noop),
    ]
