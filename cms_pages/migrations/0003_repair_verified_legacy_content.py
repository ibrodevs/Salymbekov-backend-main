from django.db import migrations


ABOUT = {
    "ru": {
        "title": "Салымбеков Университет",
        "subtitle": "Процветание через образование",
        "body": """
<p>Учреждение «Салымбеков Университет» осуществляет образовательную, научную, инновационную и научно-техническую деятельность в Кыргызской Республике.</p>
<p>Университет самостоятельно формирует свою структуру. В его составе могут действовать факультеты, институты, колледжи, школы, научные и практические подразделения, обеспечивающие образовательную, исследовательскую и иную деятельность.</p>
<p>Стратегическое развитие Университета направлено на то, чтобы качество образования, исследований, человеческих ресурсов, общественных услуг и инфраструктуры соответствовало международным стандартам.</p>
""".strip(),
    },
    "en": {
        "title": "Salymbekov University",
        "subtitle": "Prosperity through education",
        "body": """
<p>Salymbekov University is an educational institution in the Kyrgyz Republic engaged in educational, scientific, innovative and scientific-technical activities.</p>
<p>The University forms its organizational structure independently. Its structure may include faculties, institutes, colleges, schools, research and practical units supporting educational, research and other activities.</p>
<p>The strategic development of the University is aimed at ensuring that education, research, human resources, public services and infrastructure meet international standards.</p>
""".strip(),
    },
    "kg": {
        "title": "Салымбеков Университети",
        "subtitle": "Билим аркылуу өркүндөө",
        "body": """
<p>«Салымбеков Университети» мекемеси Кыргыз Республикасында билим берүү, илимий, инновациялык жана илимий-техникалык ишмердүүлүктү жүргүзөт.</p>
<p>Университет өзүнүн түзүмүн өз алдынча калыптандырат. Анын курамына факультеттер, институттар, колледждер, мектептер, илимий жана практикалык бөлүмдөр кириши мүмкүн.</p>
<p>Университеттин стратегиялык өнүгүүсү билим берүүнүн, изилдөөлөрдүн, адам ресурстарынын, коомдук кызматтардын жана инфраструктуранын сапатын эл аралык стандарттарга шайкеш келтирүүгө багытталган.</p>
""".strip(),
    },
}

MISSION = {
    "ru": {
        "title": "Миссия университета",
        "subtitle": "Миссия, стратегические цели и задачи",
        "body": """
<h2>Миссия Университета</h2>
<p><strong>Подготовка высококвалифицированных современных кадров и развитие человеческих ресурсов путем создания в Кыргызской Республике универсальной образовательной платформы.</strong></p>
<p>В рамках генеральной миссии системы образования Учреждение «Салымбеков Университет» стремится сформировать в Кыргызской Республике универсальную образовательную платформу современного высшего образования с высоким экспортным потенциалом образовательных и медицинских услуг, предоставляющую качественные образовательные услуги по международным стандартам.</p>
<h2>Стратегические цели развития</h2>
<ul>
<li>Предоставление образования и подготовка высококвалифицированных кадров по востребованным направлениям рынка труда и в соответствии с международными стандартами качества образования.</li>
<li>Развитие человеческих ресурсов, системы образования и здравоохранения страны путем открытия современных и инновационных образовательных и медицинских учреждений.</li>
<li>Превращение Университета в одну из первоклассных, инновационных и современных образовательных организаций страны с сильной материально-технической базой, качественным кадровым составом и высокой репутацией.</li>
</ul>
""".strip(),
    },
    "en": {
        "title": "University Mission",
        "subtitle": "Mission, strategic goals and objectives",
        "body": """
<h2>University Mission</h2>
<p><strong>To train highly qualified modern professionals and develop human resources by creating a universal educational platform in the Kyrgyz Republic.</strong></p>
<p>Within the general mission of the education system, Salymbekov University aims to build a universal platform for modern higher education in the Kyrgyz Republic with strong export potential for educational and medical services and education delivered according to international standards.</p>
<h2>Strategic development goals</h2>
<ul>
<li>Provide education and train highly qualified specialists in areas demanded by the labour market and in accordance with international quality standards.</li>
<li>Develop the country's human resources, education and healthcare systems by establishing modern and innovative educational and medical institutions.</li>
<li>Develop the University into one of the country's leading innovative and modern educational organizations with a strong material and technical base, qualified staff and a strong reputation.</li>
</ul>
""".strip(),
    },
    "kg": {
        "title": "Университеттин миссиясы",
        "subtitle": "Миссия, стратегиялык максаттар жана милдеттер",
        "body": """
<h2>Университеттин миссиясы</h2>
<p><strong>Кыргыз Республикасында универсалдуу билим берүү платформасын түзүү аркылуу жогорку квалификациялуу заманбап кадрларды даярдоо жана адам ресурстарын өнүктүрүү.</strong></p>
<p>Билим берүү системасынын жалпы миссиясынын алкагында «Салымбеков Университети» Кыргыз Республикасында билим берүү жана медициналык кызматтарды экспорттоо мүмкүнчүлүгү жогору, эл аралык стандарттар боюнча сапаттуу билим берген заманбап жогорку билим берүүнүн универсалдуу платформасын түзүүгө умтулат.</p>
<h2>Стратегиялык өнүгүү максаттары</h2>
<ul>
<li>Эмгек рыногунда талап кылынган багыттар боюнча жана билим берүүнүн эл аралык сапат стандарттарына ылайык жогорку квалификациялуу кадрларды даярдоо.</li>
<li>Заманбап жана инновациялык билим берүү жана медициналык мекемелерди ачуу аркылуу өлкөнүн адам ресурстарын, билим берүү жана саламаттык сактоо системаларын өнүктүрүү.</li>
<li>Университетти күчтүү материалдык-техникалык базасы, сапаттуу кадрдык курамы жана жогорку аброю бар алдыңкы инновациялык жана заманбап билим берүү уюмдарынын бирине айландыруу.</li>
</ul>
""".strip(),
    },
}

FOUNDER = {
    "ru": {
        "title": "Аскар Мааткабылович Салымбеков",
        "subtitle": "Учредитель Салымбеков Университета",
        "body": """
<p>Аскар Мааткабылович Салымбеков — один из учредителей Учреждения «Салымбеков Университет».</p>
<p>В официальных документах и соглашениях Университета он также указан как основатель и президент Совета развития Университета.</p>
<p>С его именем связано развитие образовательных, научных и общественных инициатив, направленных на создание современной образовательной среды и расширение международного сотрудничества Университета.</p>
""".strip(),
    },
    "en": {
        "title": "Askar Maatkabylovich Salymbekov",
        "subtitle": "Founder of Salymbekov University",
        "body": """
<p>Askar Maatkabylovich Salymbekov is one of the founders of Salymbekov University.</p>
<p>Official University documents and agreements also identify him as the founder and President of the University's Development Council.</p>
<p>His work is associated with the development of educational, scientific and public initiatives aimed at creating a modern learning environment and expanding the University's international cooperation.</p>
""".strip(),
    },
    "kg": {
        "title": "Аскар Мааткабылович Салымбеков",
        "subtitle": "Салымбеков Университетинин негиздөөчүсү",
        "body": """
<p>Аскар Мааткабылович Салымбеков — «Салымбеков Университети» мекемесинин негиздөөчүлөрүнүн бири.</p>
<p>Университеттин расмий документтеринде жана келишимдеринде ал Университеттин негиздөөчүсү жана Өнүктүрүү кеңешинин президенти катары да көрсөтүлгөн.</p>
<p>Анын ишмердүүлүгү заманбап билим берүү чөйрөсүн түзүүгө жана Университеттин эл аралык кызматташтыгын кеңейтүүгө багытталган билим берүү, илимий жана коомдук демилгелердин өнүгүүсү менен байланыштуу.</p>
""".strip(),
    },
}


def _apply_content(page, payload, note):
    for lang in ("ru", "en", "kg"):
        values = payload[lang]
        setattr(page, f"title_{lang}", values["title"])
        setattr(page, f"subtitle_{lang}", values["subtitle"])
        setattr(page, f"body_{lang}", values["body"])
        setattr(page, f"seo_title_{lang}", values["title"])
        setattr(page, f"seo_description_{lang}", values["subtitle"])

    data = dict(page.data or {})
    data["render_mode"] = "default"
    data["verified_legacy_source"] = True
    data["verified_legacy_source_date"] = "2026-10-17"
    page.data = data
    page.force_backend_render = True
    page.is_published = True
    page.internal_notes = note
    page.save()


def repair_verified_content(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")
    PageMedia = apps.get_model("cms_pages", "PageMedia")

    page = Page.objects.filter(path="/about").first()
    if page:
        _apply_content(
            page,
            ABOUT,
            "Проверенный контент: Положение/Устав и стратегический план Салымбеков Университета. Заглушка About удалена.",
        )

    page = Page.objects.filter(path="/university/mission").first()
    if page:
        _apply_content(
            page,
            MISSION,
            "Миссия и стратегические цели приведены к официальному стратегическому плану Салымбеков Университета.",
        )

    for path in ("/founderMessege", "/university/management/founder"):
        page = Page.objects.filter(path=path).first()
        if not page:
            continue
        _apply_content(
            page,
            FOUNDER,
            "Удалены неподтвержденные биографические факты и статистика. Оставлены сведения, подтвержденные официальными документами Университета.",
        )
        PageMedia.objects.filter(page=page, external_url__icontains="cdn-1.aki.kg").delete()

    page = Page.objects.filter(path="/MaterialBaseGallery").first()
    if page:
        page.title_ru = "Материально-техническая база"
        page.title_en = "Material and Technical Base"
        page.title_kg = "Материалдык-техникалык база"
        page.subtitle_ru = ""
        page.subtitle_en = ""
        page.subtitle_kg = ""
        page.body_ru = ""
        page.body_en = ""
        page.body_kg = ""
        page.seo_title_ru = page.title_ru
        page.seo_title_en = page.title_en
        page.seo_title_kg = page.title_kg
        page.seo_description_ru = ""
        page.seo_description_en = ""
        page.seo_description_kg = ""
        data = dict(page.data or {})
        data["render_mode"] = "default"
        data["verified_legacy_source"] = True
        data["verified_legacy_source_date"] = "2026-10-17"
        page.data = data
        page.force_backend_render = True
        page.is_published = True
        page.internal_notes = "Удален ошибочный машинный текст. Страница использует реальные CMS-медиа материально-технической базы."
        page.save()


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0002_cleanup_legacy_wordpress_media"),
    ]

    operations = [
        migrations.RunPython(repair_verified_content, migrations.RunPython.noop),
    ]
