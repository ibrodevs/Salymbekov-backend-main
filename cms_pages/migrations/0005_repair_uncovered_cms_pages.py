from django.core.management import call_command
from django.db import migrations


QUALITY_MONITORING = {
    "ru": {
        "title": "Мониторинг качества",
        "subtitle": "Внутренний мониторинг и оценка качества образования",
        "body": """
<p>Внутренний мониторинг качества образования осуществляется на основе законодательства Кыргызской Республики и нормативных правовых актов Университета, регулирующих процедуры мониторинга и оценки качества образования.</p>
<h2>Предмет оценки</h2>
<ul>
<li>учебные и внеучебные достижения обучающихся;</li>
<li>квалификация и результаты деятельности профессорско-преподавательского состава;</li>
<li>компетентность и эффективность сотрудников;</li>
<li>качество учебно-методической документации и технологий обучения;</li>
<li>реализация и качество образовательных программ.</li>
</ul>
<h2>Процедуры оценки</h2>
<p>Система менеджмента качества образования сочетает внутренние и внешние процедуры оценки. Оценка качества проводится через внутренний контроль, общественную экспертизу качества образования, лицензирование, государственную аккредитацию, государственную итоговую аттестацию выпускников и мониторинг качества образования.</p>
<h2>Источники данных</h2>
<ul>
<li>образовательная статистика;</li>
<li>текущая и итоговая аттестация;</li>
<li>мониторинговые исследования;</li>
<li>социологические опросы;</li>
<li>отчеты сотрудников Университета;</li>
<li>посещение занятий и внеучебных мероприятий.</li>
</ul>
""".strip(),
    },
    "en": {
        "title": "Quality Monitoring",
        "subtitle": "Internal monitoring and assessment of education quality",
        "body": """
<p>Internal monitoring of education quality is carried out on the basis of the legislation of the Kyrgyz Republic and the University's regulatory acts governing procedures for monitoring and assessing education quality.</p>
<h2>Assessment areas</h2>
<ul>
<li>academic and extracurricular achievements of students;</li>
<li>qualifications and performance of teaching staff;</li>
<li>competence and effectiveness of employees;</li>
<li>quality of educational and methodological documentation and learning technologies;</li>
<li>implementation and quality of educational programmes.</li>
</ul>
<h2>Assessment procedures</h2>
<p>The education quality management system combines internal and external evaluation procedures. Quality is assessed through internal control, public examination of education quality, licensing, state accreditation, state final certification of graduates and education quality monitoring.</p>
<h2>Data sources</h2>
<ul>
<li>education statistics;</li>
<li>current and final assessment;</li>
<li>monitoring studies;</li>
<li>sociological surveys;</li>
<li>reports by University employees;</li>
<li>observation of classes and extracurricular activities.</li>
</ul>
""".strip(),
    },
    "kg": {
        "title": "Сапатка мониторинг жүргүзүү",
        "subtitle": "Билим берүүнүн сапатын ички мониторингдөө жана баалоо",
        "body": """
<p>Билим берүүнүн сапатына ички мониторинг Кыргыз Республикасынын мыйзамдарынын жана билим берүүнүн сапатын мониторингдөө жана баалоо жол-жоболорун жөнгө салган Университеттин ченемдик актыларынын негизинде жүргүзүлөт.</p>
<h2>Баалоонун предмети</h2>
<ul>
<li>студенттердин окуудагы жана окуудан тышкаркы жетишкендиктери;</li>
<li>профессордук-окутуучулук курамдын квалификациясы жана ишинин натыйжалары;</li>
<li>кызматкерлердин компетенттүүлүгү жана натыйжалуулугу;</li>
<li>окуу-методикалык документтердин жана окутуу технологияларынын сапаты;</li>
<li>билим берүү программаларын ишке ашыруу жана алардын сапаты.</li>
</ul>
<h2>Баалоо жол-жоболору</h2>
<p>Билим берүүнүн сапатын башкаруу системасы ички жана тышкы баалоо жол-жоболорун айкалыштырат. Сапатты баалоо ички көзөмөл, коомдук экспертиза, лицензиялоо, мамлекеттик аккредитация, бүтүрүүчүлөрдүн мамлекеттик жыйынтыктоочу аттестациясы жана сапат мониторинги аркылуу жүргүзүлөт.</p>
<h2>Маалымат булактары</h2>
<ul>
<li>билим берүү статистикасы;</li>
<li>учурдагы жана жыйынтыктоочу аттестация;</li>
<li>мониторингдик изилдөөлөр;</li>
<li>социологиялык сурамжылоолор;</li>
<li>Университет кызматкерлеринин отчеттору;</li>
<li>сабактарга жана окуудан тышкаркы иш-чараларга катышуу.</li>
</ul>
""".strip(),
    },
}


PUBLIC_COUNCILS = {
    "ru": {
        "title": "Общественные советы",
        "subtitle": "Советы и коллегиальные органы Салымбеков Университета",
        "body": """
<p>На официальном сайте Салымбеков Университета в разделе общественных советов представлены коллегиальные органы, участвующие в управлении, развитии, обеспечении качества, научной, образовательной и общественной деятельности Университета.</p>
<ul>
<li>Совет развития;</li>
<li>Ученый совет;</li>
<li>Совет по качеству образования;</li>
<li>Учебно-методический совет;</li>
<li>Научно-технический совет;</li>
<li>Редакционный совет;</li>
<li>Приемная комиссия;</li>
<li>Комиссия по социальной поддержке;</li>
<li>Биоэтический комитет;</li>
<li>Совет молодых ученых;</li>
<li>Совет работодателей и партнеров;</li>
<li>Совет родителей;</li>
<li>Студенческий совет.</li>
</ul>
<p>Подробная информация о составе, задачах и документах каждого органа размещается на соответствующей странице сайта и управляется через CMS.</p>
""".strip(),
    },
    "en": {
        "title": "Public Councils",
        "subtitle": "Councils and collegial bodies of Salymbekov University",
        "body": """
<p>The official Salymbekov University website presents collegial bodies involved in governance, development, quality assurance, research, education and public activity of the University.</p>
<ul>
<li>Development Council;</li>
<li>Academic Council;</li>
<li>Education Quality Council;</li>
<li>Educational and Methodological Council;</li>
<li>Scientific and Technical Council;</li>
<li>Editorial Council;</li>
<li>Admissions Committee;</li>
<li>Social Support Commission;</li>
<li>Bioethics Committee;</li>
<li>Council of Young Scientists;</li>
<li>Employers and Partners Council;</li>
<li>Parents Council;</li>
<li>Student Council.</li>
</ul>
<p>Information about the composition, functions and documents of each body is published on its corresponding page and managed through the CMS.</p>
""".strip(),
    },
    "kg": {
        "title": "Коомдук кеңештер",
        "subtitle": "Салымбеков Университетинин кеңештери жана коллегиалдык органдары",
        "body": """
<p>Салымбеков Университетинин расмий сайтында Университетти башкарууга, өнүктүрүүгө, сапатты камсыздоого, илимий, билим берүү жана коомдук ишмердүүлүккө катышкан коллегиалдык органдар көрсөтүлөт.</p>
<ul>
<li>Өнүктүрүү кеңеши;</li>
<li>Окумуштуулар кеңеши;</li>
<li>Билим берүүнүн сапаты боюнча кеңеш;</li>
<li>Окуу-методикалык кеңеш;</li>
<li>Илимий-техникалык кеңеш;</li>
<li>Редакциялык кеңеш;</li>
<li>Кабыл алуу комиссиясы;</li>
<li>Социалдык колдоо комиссиясы;</li>
<li>Биоэтика комитети;</li>
<li>Жаш окумуштуулар кеңеши;</li>
<li>Иш берүүчүлөр жана өнөктөштөр кеңеши;</li>
<li>Ата-энелер кеңеши;</li>
<li>Студенттик кеңеш.</li>
</ul>
<p>Ар бир органдын курамы, милдеттери жана документтери тиешелүү баракта жарыяланып, CMS аркылуу башкарылат.</p>
""".strip(),
    },
}


DOUBLE_DIPLOMA = {
    "ru": {
        "title": "Программа двойного диплома",
        "subtitle": "Международный колледж IT и бизнеса и Lincoln University College, Малайзия",
        "body": """
<p>Международный колледж IT и бизнеса Салымбеков Университета реализует программу двойного диплома совместно с Lincoln University College (Малайзия).</p>
<h2>Направления</h2>
<ul>
<li>Computer Science — компьютерные науки;</li>
<li>Multimedia Applications — мультимедийные приложения;</li>
<li>Mobile Computing — мобильные вычисления.</li>
</ul>
<h2>Формат обучения</h2>
<ul>
<li>на базе 9 классов: 2 года обучения в Кыргызстане и 1,5 года в Малайзии;</li>
<li>на базе 11 классов: 1 год обучения в Кыргызстане и 1,5 года в Малайзии.</li>
</ul>
<p>После успешного завершения программы выпускники получают два диплома — Салымбеков Университета и Lincoln University College. Программа дает студентам международный академический опыт и возможность продолжить образование и профессиональное развитие за рубежом.</p>
""".strip(),
    },
    "en": {
        "title": "Double Degree Programme",
        "subtitle": "International College of IT and Business and Lincoln University College, Malaysia",
        "body": """
<p>The International College of IT and Business of Salymbekov University implements a double degree programme together with Lincoln University College in Malaysia.</p>
<h2>Programmes</h2>
<ul>
<li>Computer Science;</li>
<li>Multimedia Applications;</li>
<li>Mobile Computing.</li>
</ul>
<h2>Study format</h2>
<ul>
<li>after Grade 9: 2 years in Kyrgyzstan and 1.5 years in Malaysia;</li>
<li>after Grade 11: 1 year in Kyrgyzstan and 1.5 years in Malaysia.</li>
</ul>
<p>After successful completion, graduates receive two diplomas — from Salymbekov University and Lincoln University College. The programme provides international academic experience and opportunities for further study and professional development abroad.</p>
""".strip(),
    },
    "kg": {
        "title": "Кош диплом программасы",
        "subtitle": "Эл аралык IT жана бизнес колледжи жана Lincoln University College, Малайзия",
        "body": """
<p>Салымбеков Университетинин Эл аралык IT жана бизнес колледжи Малайзиядагы Lincoln University College менен биргеликте кош диплом программасын ишке ашырат.</p>
<h2>Багыттар</h2>
<ul>
<li>Computer Science — компьютердик илимдер;</li>
<li>Multimedia Applications — мультимедиялык колдонмолор;</li>
<li>Mobile Computing — мобилдик эсептөөлөр.</li>
</ul>
<h2>Окуу форматы</h2>
<ul>
<li>9-класстын базасында: 2 жыл Кыргызстанда жана 1,5 жыл Малайзияда;</li>
<li>11-класстын базасында: 1 жыл Кыргызстанда жана 1,5 жыл Малайзияда.</li>
</ul>
<p>Программаны ийгиликтүү аяктаган бүтүрүүчүлөр Салымбеков Университетинин жана Lincoln University College'дин эки дипломун алышат. Программа эл аралык академиялык тажрыйбага жана чет өлкөдө билим алууну жана кесиптик өнүгүүнү улантууга мүмкүнчүлүк берет.</p>
""".strip(),
    },
}


SIMULATION_CENTER = {
    "ru": {
        "title": "Симуляционный центр",
        "subtitle": "Практическая подготовка студентов медицинских программ",
        "body": """
<p>Симуляционный центр входит в перечень материально-технического обеспечения образовательных программ медицинского направления Салымбеков Университета.</p>
<p>В официальной основной образовательной программе Университета симуляционный центр указан наряду с профильными лабораториями, анатомическим музеем, кабинетами и аудиториями, необходимыми для практической подготовки будущих медицинских специалистов.</p>
""".strip(),
    },
    "en": {
        "title": "Simulation Center",
        "subtitle": "Practical training for students of medical programmes",
        "body": """
<p>The Simulation Center is included in the material and technical facilities supporting Salymbekov University's medical education programmes.</p>
<p>The University's official educational programme lists the Simulation Center together with specialised laboratories, an anatomy museum, classrooms and facilities required for the practical training of future medical professionals.</p>
""".strip(),
    },
    "kg": {
        "title": "Симуляциялык борбор",
        "subtitle": "Медициналык программалардын студенттерин практикалык даярдоо",
        "body": """
<p>Симуляциялык борбор Салымбеков Университетинин медициналык багыттагы билим берүү программаларынын материалдык-техникалык камсыздоосуна кирет.</p>
<p>Университеттин расмий негизги билим берүү программасында симуляциялык борбор келечектеги медицина адистерин практикалык даярдоо үчүн керектүү адистештирилген лабораториялар, анатомиялык музей, кабинеттер жана аудиториялар менен бирге көрсөтүлгөн.</p>
""".strip(),
    },
}


VACANCIES = {
    "ru": {
        "title": "Вакансии",
        "subtitle": "Карьера в Салымбеков Университете",
        "body": """
<p>Этот раздел предназначен для публикации актуальных вакансий Салымбеков Университета.</p>
<p>Чтобы не показывать устаревшие объявления со старого сайта, исторический список вакансий не переносится автоматически. Новые вакансии и условия по ним добавляются администрацией Университета через CMS.</p>
<p>По общим вопросам: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
    "en": {
        "title": "Vacancies",
        "subtitle": "Careers at Salymbekov University",
        "body": """
<p>This section is used to publish current vacancies at Salymbekov University.</p>
<p>To avoid displaying outdated announcements from the old website, historical vacancy listings are not copied automatically. New vacancies and their conditions are managed by the University administration through the CMS.</p>
<p>General enquiries: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
    "kg": {
        "title": "Бош орундар",
        "subtitle": "Салымбеков Университетиндеги карьера",
        "body": """
<p>Бул бөлүм Салымбеков Университетиндеги актуалдуу бош орундарды жарыялоо үчүн колдонулат.</p>
<p>Эски сайттагы мөөнөтү өтүп кеткен жарыяларды көрсөтпөө үчүн тарыхый вакансиялар автоматтык түрдө көчүрүлбөйт. Жаңы бош орундар жана алардын шарттары Университеттин администрациясы тарабынан CMS аркылуу башкарылат.</p>
<p>Жалпы суроолор боюнча: <a href="mailto:info@salymbekov.com">info@salymbekov.com</a>, +996 (312) 65 85 38.</p>
""".strip(),
    },
}


LICENSES = {
    "ru": {
        "title": "Лицензии и свидетельства",
        "subtitle": "Официальные регистрационные и разрешительные документы Университета",
        "body": """
<p>На старом официальном сайте Салымбеков Университета действовал отдельный раздел «Лицензии и свидетельства». В новой CMS этот раздел хранит только подтвержденные документы и их изображения.</p>
<p>Фиктивные номера документов из старого frontend-компонента удалены и не используются.</p>
""".strip(),
    },
    "en": {
        "title": "Licences and Certificates",
        "subtitle": "Official registration and authorisation documents of the University",
        "body": """
<p>The former official Salymbekov University website contained a dedicated Licences and Certificates section. The new CMS stores only verified documents and their images.</p>
<p>Placeholder document numbers from the old frontend component have been removed and are not used.</p>
""".strip(),
    },
    "kg": {
        "title": "Лицензиялар жана күбөлүктөр",
        "subtitle": "Университеттин расмий каттоо жана уруксат берүүчү документтери",
        "body": """
<p>Салымбеков Университетинин мурдагы расмий сайтында «Лицензиялар жана күбөлүктөр» деген өзүнчө бөлүм болгон. Жаңы CMSте текшерилген документтер жана алардын сүрөттөрү гана сакталат.</p>
<p>Эски frontend-компоненттеги шарттуу документ номерлери өчүрүлдү жана колдонулбайт.</p>
""".strip(),
    },
}


BRANDBOOK = {
    "ru": {
        "title": "Брендбук",
        "subtitle": "Официальные правила визуального стиля Салымбеков Университета",
        "body": """
<p>Брендбук содержит правила использования фирменного стиля и визуальной айдентики Салымбеков Университета.</p>
<p>Официальный файл брендбука перенесен со старого сайта в систему документов CMS.</p>
""".strip(),
    },
    "en": {
        "title": "Brandbook",
        "subtitle": "Official Salymbekov University visual identity guidelines",
        "body": """
<p>The brandbook contains guidelines for using the Salymbekov University visual identity and corporate style.</p>
<p>The official brandbook file has been transferred from the old website into the CMS document system.</p>
""".strip(),
    },
    "kg": {
        "title": "Брендбук",
        "subtitle": "Салымбеков Университетинин визуалдык стилин колдонуу боюнча расмий эрежелер",
        "body": """
<p>Брендбук Салымбеков Университетинин фирмалык стилин жана визуалдык айдентикасын колдонуу эрежелерин камтыйт.</p>
<p>Брендбуктун расмий файлы эски сайттан CMSтин документтер системасына көчүрүлдү.</p>
""".strip(),
    },
}


PAGES = {
    "/university/quality-management-system/quality-monitoring": (
        QUALITY_MONITORING,
        ["https://salymbekov.com/ru/monitoring-kachestva/", "https://salymbekov.com/en/monitoring-kachestva/"],
    ),
    "/university/management/public-councils": (
        PUBLIC_COUNCILS,
        ["https://salymbekov.com/ru/monitoring-kachestva/"],
    ),
    "/education/it-college/double-diploma": (
        DOUBLE_DIPLOMA,
        ["https://salymbekov.com/ru/programma-dvoinogo-diploma/", "https://www.lincoln.edu.my/"],
    ),
    "/clinical/simulation-center": (
        SIMULATION_CENTER,
        ["https://salymbekov.com/wp-content/uploads/2022/06/oop-6let-2-versija.pdf"],
    ),
    "/vacancies": (
        VACANCIES,
        ["https://salymbekov.com/ru/vakansii/", "https://salymbekov.com/ru/kontakty/"],
    ),
    "/university/normative-docs/licenses": (
        LICENSES,
        ["https://salymbekov.com/ru/licenzii/"],
    ),
    "/university/normative-docs/logo": (
        BRANDBOOK,
        ["https://salymbekov.com/wp-content/uploads/2023/10/brjendbuk_organized_new.pdf"],
    ),
}


def apply_content(page, payload, source_urls):
    for lang in ("ru", "en", "kg"):
        values = payload[lang]
        setattr(page, f"title_{lang}", values["title"])
        setattr(page, f"subtitle_{lang}", values["subtitle"])
        setattr(page, f"body_{lang}", values["body"])
        setattr(page, f"seo_title_{lang}", values["title"])
        setattr(page, f"seo_description_{lang}", values["subtitle"])

    data = dict(page.data or {})
    data["render_mode"] = "default"
    data["verified_source_urls"] = source_urls
    data["verified_source_date"] = "2026-10-17"
    page.data = data
    page.force_backend_render = True
    page.is_published = True
    page.internal_notes = "Контент восстановлен только из подтвержденных источников. Старые frontend-заглушки и неподтвержденные цифры не переносились."
    page.save()


def repair_uncovered_pages(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")
    PageMedia = apps.get_model("cms_pages", "PageMedia")
    PageDocument = apps.get_model("cms_pages", "PageDocument")

    for path, (payload, source_urls) in PAGES.items():
        page = Page.objects.filter(path=path).first()
        if not page:
            continue
        apply_content(page, payload, source_urls)

    licenses = Page.objects.filter(path="/university/normative-docs/licenses").first()
    if licenses:
        license_image = "https://salymbekov.com/wp-content/uploads/2021/04/img4-rotated.jpg"
        if not PageMedia.objects.filter(page=licenses, external_url=license_image).exists():
            PageMedia.objects.create(
                page=licenses,
                media_type="image",
                external_url=license_image,
                is_hero=False,
                order=10,
                title_ru="Лицензия / свидетельство",
                title_en="Licence / certificate",
                title_kg="Лицензия / күбөлүк",
                alt_text_ru="Официальный документ Салымбеков Университета",
                alt_text_en="Official Salymbekov University document",
                alt_text_kg="Салымбеков Университетинин расмий документи",
            )

    brandbook = Page.objects.filter(path="/university/normative-docs/logo").first()
    if brandbook:
        brandbook_url = "https://salymbekov.com/wp-content/uploads/2023/10/brjendbuk_organized_new.pdf"
        if not PageDocument.objects.filter(page=brandbook, external_url=brandbook_url).exists():
            PageDocument.objects.create(
                page=brandbook,
                external_url=brandbook_url,
                order=10,
                title_ru="Брендбук Салымбеков Университета",
                title_en="Salymbekov University Brandbook",
                title_kg="Салымбеков Университетинин брендбугу",
            )

    # These legacy files are added by this migration after the earlier one-time
    # cleanup migration has already run, so give them one final migration pass.
    try:
        call_command("migrate_external_media", "--apply", "--timeout", "15")
    except Exception as exc:
        print(f"Final legacy media migration skipped/partial: {exc}")


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0004_repair_services_and_contacts"),
    ]

    operations = [
        migrations.RunPython(repair_uncovered_pages, migrations.RunPython.noop),
    ]
