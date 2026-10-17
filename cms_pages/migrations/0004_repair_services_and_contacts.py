from django.db import migrations


SERVICES = {
    "ru": {
        "title": "Образовательные услуги",
        "subtitle": "Основные направления образовательной деятельности Салымбеков Университета",
        "body": """
<p>Учреждение «Салымбеков Университет» осуществляет образовательную деятельность по программам общего, профессионального, среднего профессионального, высшего профессионального и послевузовского профессионального образования в соответствии с лицензиями и законодательством Кыргызской Республики.</p>
<h2>Основные направления</h2>
<ul>
<li>высшее профессиональное образование;</li>
<li>среднее профессиональное образование;</li>
<li>послевузовское профессиональное образование, включая подготовку научных и научно-педагогических кадров;</li>
<li>профессиональная подготовка, переподготовка и повышение квалификации;</li>
<li>дополнительные образовательные программы;</li>
<li>научная, исследовательская и инновационная деятельность.</li>
</ul>
<p>Конкретные программы, условия обучения и документы представлены в соответствующих образовательных разделах сайта.</p>
""".strip(),
    },
    "en": {
        "title": "Educational Services",
        "subtitle": "Main areas of educational activity at Salymbekov University",
        "body": """
<p>Salymbekov University provides educational programmes in general, vocational, secondary vocational, higher professional and postgraduate professional education in accordance with its licences and the legislation of the Kyrgyz Republic.</p>
<h2>Main areas</h2>
<ul>
<li>higher professional education;</li>
<li>secondary vocational education;</li>
<li>postgraduate professional education, including training of scientific and academic personnel;</li>
<li>professional training, retraining and advanced training;</li>
<li>additional educational programmes;</li>
<li>scientific, research and innovation activities.</li>
</ul>
<p>Specific programmes, study conditions and documents are available in the relevant educational sections of the website.</p>
""".strip(),
    },
    "kg": {
        "title": "Билим берүү кызматтары",
        "subtitle": "Салымбеков Университетинин билим берүү ишмердүүлүгүнүн негизги багыттары",
        "body": """
<p>«Салымбеков Университети» мекемеси Кыргыз Республикасынын мыйзамдарына жана лицензияларына ылайык жалпы, кесиптик, орто кесиптик, жогорку кесиптик жана жогорку окуу жайдан кийинки кесиптик билим берүү программаларын ишке ашырат.</p>
<h2>Негизги багыттар</h2>
<ul>
<li>жогорку кесиптик билим берүү;</li>
<li>орто кесиптик билим берүү;</li>
<li>илимий жана илимий-педагогикалык кадрларды даярдоону камтыган жогорку окуу жайдан кийинки кесиптик билим берүү;</li>
<li>кесиптик даярдоо, кайра даярдоо жана квалификацияны жогорулатуу;</li>
<li>кошумча билим берүү программалары;</li>
<li>илимий, изилдөө жана инновациялык ишмердүүлүк.</li>
</ul>
<p>Так программалар, окуу шарттары жана документтер сайттын тиешелүү билим берүү бөлүмдөрүндө берилген.</p>
""".strip(),
    },
}

CONTACTS = {
    "ru": {
        "title": "Контакты",
        "subtitle": "Контактная информация Салымбеков Университета",
        "body": """
<h2>Салымбеков Университет</h2>
<p><strong>Фактический адрес:</strong> Кыргызская Республика, г. Бишкек, ул. Ю. Фучика, 3</p>
<p><strong>Юридический адрес:</strong> Кыргызская Республика, г. Бишкек, ул. Ибраимова, 115А</p>
<p><strong>Телефон:</strong> +996 (312) 65 85 38</p>
<p><strong>Email:</strong> <a href="mailto:info@salymbekov.com">info@salymbekov.com</a></p>
<p><strong>Сайт:</strong> <a href="https://salymbekov.com/" target="_blank" rel="noopener noreferrer">salymbekov.com</a></p>
""".strip(),
    },
    "en": {
        "title": "Contacts",
        "subtitle": "Contact information for Salymbekov University",
        "body": """
<h2>Salymbekov University</h2>
<p><strong>Actual address:</strong> 3 Y. Fuchik St., Bishkek, Kyrgyz Republic</p>
<p><strong>Legal address:</strong> 115A Ibraimov St., Bishkek, Kyrgyz Republic</p>
<p><strong>Phone:</strong> +996 (312) 65 85 38</p>
<p><strong>Email:</strong> <a href="mailto:info@salymbekov.com">info@salymbekov.com</a></p>
<p><strong>Website:</strong> <a href="https://salymbekov.com/" target="_blank" rel="noopener noreferrer">salymbekov.com</a></p>
""".strip(),
    },
    "kg": {
        "title": "Байланыштар",
        "subtitle": "Салымбеков Университетинин байланыш маалыматы",
        "body": """
<h2>Салымбеков Университети</h2>
<p><strong>Иш жүзүндөгү дарек:</strong> Кыргыз Республикасы, Бишкек ш., Ю. Фучик көч., 3</p>
<p><strong>Юридикалык дарек:</strong> Кыргыз Республикасы, Бишкек ш., Ибраимов көч., 115А</p>
<p><strong>Телефон:</strong> +996 (312) 65 85 38</p>
<p><strong>Email:</strong> <a href="mailto:info@salymbekov.com">info@salymbekov.com</a></p>
<p><strong>Сайт:</strong> <a href="https://salymbekov.com/" target="_blank" rel="noopener noreferrer">salymbekov.com</a></p>
""".strip(),
    },
}


def apply_content(page, payload, note):
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


def repair_services_and_contacts(apps, schema_editor):
    Page = apps.get_model("cms_pages", "Page")

    services = Page.objects.filter(path="/services").first()
    if services:
        apply_content(
            services,
            SERVICES,
            "Удалена frontend-заглушка. Направления образовательной деятельности приведены к официальному Положению об Учреждении «Салымбеков Университет».",
        )

    for path in ("/contact", "/contacts"):
        page = Page.objects.filter(path=path).first()
        if not page:
            continue
        apply_content(
            page,
            CONTACTS,
            "Контактные данные сверены с публичными страницами salymbekov.com и официальными договорами Университета: фактический адрес Фучика 3, юридический адрес Ибраимова 115А.",
        )


class Migration(migrations.Migration):
    dependencies = [
        ("cms_pages", "0003_repair_verified_legacy_content"),
    ]

    operations = [
        migrations.RunPython(repair_services_and_contacts, migrations.RunPython.noop),
    ]
