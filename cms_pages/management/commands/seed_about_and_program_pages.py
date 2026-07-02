import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from cms_pages.models import Page, PageCard, PageDocument, PageMedia, PageSection


def text_to_html(value):
    if not value:
        return ""

    lines = [line.strip() for line in str(value).splitlines() if line.strip()]
    if not lines:
        return ""

    html_parts = []
    for line in lines:
        if line.startswith("<strong>") and line.endswith("</strong>"):
            html_parts.append(f"<p>{line}</p>")
        else:
            html_parts.append(f"<p>{line}</p>")
    return "".join(html_parts)


def list_to_html(items):
    normalized = [item.strip() for item in items if item and str(item).strip()]
    if not normalized:
        return ""
    return "<ul>" + "".join(f"<li>{item}</li>" for item in normalized) + "</ul>"


def safe_get(data, key, default=""):
    current = data
    for part in key.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    return current


class Command(BaseCommand):
    help = "Seeds structured CMS content for /about and priority program pages, optionally uploading external assets into storage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag the command only prints what would change.",
        )
        parser.add_argument(
            "--download-assets",
            action="store_true",
            help="Download external images/files into Django storage instead of keeping remote URLs.",
        )
        parser.add_argument(
            "--only-path",
            action="append",
            default=[],
            help="Limit execution to one or more page paths.",
        )

    def handle(self, *args, **options):
        self.apply = options["apply"]
        self.download_assets = options["download_assets"]

        backend_root = Path(__file__).resolve().parents[3]
        frontend_root = backend_root.parent / "salymbekov-frontend"

        translations = self.load_translations(frontend_root)
        page_configs = self.build_page_configs(translations)

        selected_paths = set(options["only_path"] or [])
        if selected_paths:
            page_configs = [cfg for cfg in page_configs if cfg["path"] in selected_paths]

        if not page_configs:
            self.stdout.write(self.style.WARNING("No matching page configs selected."))
            return

        for config in page_configs:
            self.seed_page(config)

    def load_translations(self, frontend_root):
        translations = {}
        for lang in ("ru", "en", "kg"):
            locale_path = frontend_root / "src" / "locales" / lang / "translation.json"
            translations[lang] = json.loads(locale_path.read_text(encoding="utf-8"))
        return translations

    def build_page_configs(self, translations):
        return [
            self.build_about_page(),
            self.build_five_years_page(translations),
            self.build_six_years_page(translations),
            self.build_software_development_page(translations),
            self.build_mobile_computing_page(translations),
            self.build_multimedia_apps_page(translations),
        ]

    def build_about_page(self):
        return {
            "path": "/about",
            "admin_title": "About",
            "navigation_group": "about",
            "badge": {"ru": "О нас", "en": "About us", "kg": "Биз жөнүндө"},
            "title": {"ru": "О нас", "en": "About us", "kg": "Биз жөнүндө"},
            "subtitle": {
                "ru": "Ключевая информация об университете, его миссии, структуре и основных документах.",
                "en": "Key information about the university, its mission, structure, and core documents.",
                "kg": "Университет, анын миссиясы, түзүмү жана негизги документтери тууралуу негизги маалымат.",
            },
            "body": {
                "ru": (
                    "<p>Раздел объединяет базовую информацию об Университете Салымбекова. "
                    "Ниже собраны основные направления, которые чаще всего нужны посетителям сайта.</p>"
                    "<p><a href=\"/university/mission\">Миссия и цели</a> · "
                    "<a href=\"/university/structure\">Структура</a> · "
                    "<a href=\"/university/management\">Управление</a> · "
                    "<a href=\"/university/normative-docs\">Нормативные документы</a></p>"
                ),
                "en": (
                    "<p>This section brings together the core information about Salymbekov University. "
                    "Below are the main directions that visitors usually need first.</p>"
                    "<p><a href=\"/university/mission\">Mission and goals</a> · "
                    "<a href=\"/university/structure\">Structure</a> · "
                    "<a href=\"/university/management\">Management</a> · "
                    "<a href=\"/university/normative-docs\">Normative documents</a></p>"
                ),
                "kg": (
                    "<p>Бул бөлүм Салымбеков университети тууралуу негизги маалыматты бир жерге топтойт. "
                    "Төмөндө сайттын конокторуна эң көп керек болгон багыттар берилген.</p>"
                    "<p><a href=\"/university/mission\">Миссия жана максаттар</a> · "
                    "<a href=\"/university/structure\">Түзүм</a> · "
                    "<a href=\"/university/management\">Башкаруу</a> · "
                    "<a href=\"/university/normative-docs\">Нормативдик документтер</a></p>"
                ),
            },
            "cards": [
                {
                    "title": {
                        "ru": "Миссия и цели",
                        "en": "Mission and goals",
                        "kg": "Миссия жана максаттар",
                    },
                    "text": {
                        "ru": "Узнайте о стратегическом направлении университета и его образовательных приоритетах.",
                        "en": "Learn about the strategic direction of the university and its educational priorities.",
                        "kg": "Университеттин стратегиялык багыты жана билим берүү приоритеттери тууралуу билиңиз.",
                    },
                },
                {
                    "title": {
                        "ru": "Структура",
                        "en": "Structure",
                        "kg": "Түзүм",
                    },
                    "text": {
                        "ru": "Обзор ключевых подразделений, факультетов и внутренних академических единиц.",
                        "en": "An overview of the key departments, faculties, and internal academic units.",
                        "kg": "Негизги бөлүмдөрдүн, факультеттердин жана ички академиялык бирдиктердин сереби.",
                    },
                },
                {
                    "title": {
                        "ru": "Управление",
                        "en": "Management",
                        "kg": "Башкаруу",
                    },
                    "text": {
                        "ru": "Информация о руководстве университета и системе принятия решений.",
                        "en": "Information about the university leadership and decision-making structure.",
                        "kg": "Университеттин жетекчилиги жана чечим кабыл алуу түзүмү жөнүндө маалымат.",
                    },
                },
                {
                    "title": {
                        "ru": "Нормативные документы",
                        "en": "Normative documents",
                        "kg": "Нормативдик документтер",
                    },
                    "text": {
                        "ru": "Лицензии, внутренние положения и другие важные документы для посетителей сайта.",
                        "en": "Licenses, internal regulations, and other important documents for site visitors.",
                        "kg": "Лицензиялар, ички жоболор жана сайттын коноктору үчүн башка маанилүү документтер.",
                    },
                },
            ],
            "sections": [],
            "media": [],
            "documents": [],
        }

    def build_five_years_page(self, translations):
        return {
            "path": "/education/mfm/programs/five-years",
            "admin_title": "Education / Mfm / Programs / Five Years",
            "navigation_group": "education",
            "badge": self.translated(translations, "generalMedicine.badge"),
            "title": self.translated(translations, "generalMedicine.title"),
            "subtitle": self.translated(translations, "generalMedicine.subtitle"),
            "body": {
                lang: (
                    text_to_html(safe_get(translations[lang], "generalMedicine.introduction"))
                    + text_to_html(safe_get(translations[lang], "generalMedicine.programInfo"))
                )
                for lang in ("ru", "en", "kg")
            },
            "sections": [
                {
                    "title": self.translated(translations, "generalMedicine.programGoal"),
                    "body": {
                        lang: text_to_html(safe_get(translations[lang], "generalMedicine.programDescription"))
                        for lang in ("ru", "en", "kg")
                    },
                },
                {
                    "title": self.translated(translations, "generalMedicine.professionalActivities"),
                    "body": {
                        lang: text_to_html(safe_get(translations[lang], "generalMedicine.programDescription"))
                        for lang in ("ru", "en", "kg")
                    },
                },
            ],
            "cards": [
                self.card_from_keys(translations, "generalMedicine.features.clinical.title", "generalMedicine.features.clinical.description"),
                self.card_from_keys(translations, "generalMedicine.features.practical.title", "generalMedicine.features.practical.description"),
                self.card_from_keys(translations, "generalMedicine.features.international.title", "generalMedicine.features.international.description"),
                self.card_from_keys(translations, "generalMedicine.features.quality.title", "generalMedicine.features.quality.description"),
            ],
            "media": [
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b6732.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b6708.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b6617.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b5048.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b6580.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b5031.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b5004.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b5012.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b4697.jpg",
                "https://salymbekov.com/wp-content/uploads/2023/03/bc0b4673.jpg",
            ],
            "documents": [
                {
                    "url": "https://salymbekov.com/wp-content/uploads/2024/01/curriculum-general-medicine.pdf",
                    "title": self.translated(translations, "generalMedicine.curriculumButton"),
                }
            ],
        }

    def build_six_years_page(self, translations):
        return {
            "path": "/education/mfm/programs/six-years",
            "admin_title": "Education / Mfm / Programs / Six Years",
            "navigation_group": "education",
            "badge": self.translated(translations, "education.mfm.programs.6age.badge"),
            "title": self.translated(translations, "education.mfm.programs.6age.title"),
            "subtitle": self.translated(translations, "education.mfm.programs.6age.subtitle"),
            "body": {"ru": "", "en": "", "kg": ""},
            "sections": [
                {
                    "title": self.translated(translations, "education.mfm.programs.6age.curriculum.academic.title"),
                    "body": {
                        lang: list_to_html(safe_get(translations[lang], "education.mfm.programs.6age.curriculum.academic.items", []))
                        for lang in ("ru", "en", "kg")
                    },
                },
                {
                    "title": self.translated(translations, "education.mfm.programs.6age.curriculum.creative.title"),
                    "body": {
                        lang: list_to_html(safe_get(translations[lang], "education.mfm.programs.6age.curriculum.creative.items", []))
                        for lang in ("ru", "en", "kg")
                    },
                },
                {
                    "title": self.translated(translations, "education.mfm.programs.6age.curriculum.physical.title"),
                    "body": {
                        lang: list_to_html(safe_get(translations[lang], "education.mfm.programs.6age.curriculum.physical.items", []))
                        for lang in ("ru", "en", "kg")
                    },
                },
            ],
            "cards": [
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.features.earlyDevelopment.title",
                    "education.mfm.programs.6age.features.earlyDevelopment.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.features.comprehensiveLearning.title",
                    "education.mfm.programs.6age.features.comprehensiveLearning.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.features.socialSkills.title",
                    "education.mfm.programs.6age.features.socialSkills.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.features.healthCare.title",
                    "education.mfm.programs.6age.features.healthCare.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.admission.consultation.title",
                    "education.mfm.programs.6age.admission.consultation.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.admission.assessment.title",
                    "education.mfm.programs.6age.admission.assessment.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.admission.enrollment.title",
                    "education.mfm.programs.6age.admission.enrollment.description",
                ),
                self.card_from_keys(
                    translations,
                    "education.mfm.programs.6age.admission.orientation.title",
                    "education.mfm.programs.6age.admission.orientation.description",
                ),
            ],
            "media": [],
            "documents": [],
        }

    def build_software_development_page(self, translations):
        return {
            "path": "/education/it-college/specialties/diplom-computational-sciences",
            "admin_title": "Education / It College / Specialties / Diplom Computational Sciences",
            "navigation_group": "education",
            "badge": self.translated(translations, "softwareDevelopment.badge"),
            "title": self.translated(translations, "softwareDevelopment.title"),
            "subtitle": self.translated(translations, "softwareDevelopment.subtitle"),
            "body": {
                lang: (
                    text_to_html(safe_get(translations[lang], "softwareDevelopment.programGoal.content"))
                    + text_to_html(safe_get(translations[lang], "softwareDevelopment.programDescription.content"))
                )
                for lang in ("ru", "en", "kg")
            },
            "sections": [
                {
                    "title": self.translated(translations, "softwareDevelopment.itEducation.title"),
                    "body": {
                        lang: text_to_html(safe_get(translations[lang], "softwareDevelopment.itEducation.content"))
                        for lang in ("ru", "en", "kg")
                    },
                },
                {
                    "title": self.translated(translations, "softwareDevelopment.careerOpportunities.title"),
                    "body": {
                        lang: text_to_html(safe_get(translations[lang], "softwareDevelopment.careerOpportunities.content"))
                        for lang in ("ru", "en", "kg")
                    },
                },
            ],
            "cards": [
                self.card_from_keys(translations, "softwareDevelopment.careers.frontend.title", "softwareDevelopment.careers.frontend.description", "softwareDevelopment.careers.frontend.salary"),
                self.card_from_keys(translations, "softwareDevelopment.careers.backend.title", "softwareDevelopment.careers.backend.description", "softwareDevelopment.careers.backend.salary"),
                self.card_from_keys(translations, "softwareDevelopment.careers.mobile.title", "softwareDevelopment.careers.mobile.description", "softwareDevelopment.careers.mobile.salary"),
                self.card_from_keys(translations, "softwareDevelopment.careers.database.title", "softwareDevelopment.careers.database.description", "softwareDevelopment.careers.database.salary"),
            ],
            "media": [
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2481.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2512.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2476.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2487.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2574.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2662.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2562.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2577.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2674.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2664.jpg",
            ],
            "documents": [],
        }

    def build_mobile_computing_page(self, translations):
        return {
            "path": "/education/it-college/specialties/diplom-mobile-computing",
            "admin_title": "Education / It College / Specialties / Diplom Mobile Computing",
            "navigation_group": "education",
            "badge": self.translated(translations, "mobileComputing.badge"),
            "title": self.translated(translations, "mobileComputing.title"),
            "subtitle": self.translated(translations, "mobileComputing.subtitle"),
            "body": {
                lang: (
                    text_to_html(safe_get(translations[lang], "mobileComputing.overview.content"))
                    + text_to_html(safe_get(translations[lang], "mobileComputing.programGoal.content"))
                    + text_to_html(safe_get(translations[lang], "mobileComputing.specialist.content"))
                )
                for lang in ("ru", "en", "kg")
            },
            "sections": [
                {
                    "title": self.translated(translations, "mobileComputing.platforms.title"),
                    "body": {
                        lang: list_to_html(
                            [
                                safe_get(translations[lang], "mobileComputing.platforms.androidDesc"),
                                safe_get(translations[lang], "mobileComputing.platforms.iosDesc"),
                                safe_get(translations[lang], "mobileComputing.platforms.reactDesc"),
                                safe_get(translations[lang], "mobileComputing.platforms.flutterDesc"),
                                safe_get(translations[lang], "mobileComputing.platforms.backendDesc"),
                                safe_get(translations[lang], "mobileComputing.platforms.cloudDesc"),
                            ]
                        )
                        for lang in ("ru", "en", "kg")
                    },
                },
                {
                    "title": self.translated(translations, "mobileComputing.careerOpportunities.title"),
                    "body": {
                        lang: text_to_html(safe_get(translations[lang], "mobileComputing.careerOpportunities.content"))
                        for lang in ("ru", "en", "kg")
                    },
                },
            ],
            "cards": [
                self.card_from_keys(translations, "mobileComputing.careers.android.title", "mobileComputing.careers.android.description", "mobileComputing.careers.android.salary"),
                self.card_from_keys(translations, "mobileComputing.careers.ios.title", "mobileComputing.careers.ios.description", "mobileComputing.careers.ios.salary"),
                self.card_from_keys(translations, "mobileComputing.careers.crossplatform.title", "mobileComputing.careers.crossplatform.description", "mobileComputing.careers.crossplatform.salary"),
                self.card_from_keys(translations, "mobileComputing.careers.mobileBackend.title", "mobileComputing.careers.mobileBackend.description", "mobileComputing.careers.mobileBackend.salary"),
            ],
            "media": [
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2481.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2512.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2476.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2487.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2574.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2662.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2562.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2577.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2674.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2664.jpg",
            ],
            "documents": [],
        }

    def build_multimedia_apps_page(self, translations):
        return {
            "path": "/education/it-college/specialties/diplom-multimedia-applications",
            "admin_title": "Education / It College / Specialties / Diplom Multimedia Applications",
            "navigation_group": "education",
            "badge": self.translated(translations, "mobileDevelopment.badge"),
            "title": self.translated(translations, "mobileDevelopment.title"),
            "subtitle": self.translated(translations, "mobileDevelopment.subtitle"),
            "body": {
                lang: (
                    text_to_html(safe_get(translations[lang], "mobileDevelopment.overview.content"))
                    + text_to_html(safe_get(translations[lang], "mobileDevelopment.programGoal.content"))
                )
                for lang in ("ru", "en", "kg")
            },
            "sections": [],
            "cards": [
                self.card_from_keys(translations, "mobileDevelopment.features.mobile.title", "mobileDevelopment.features.mobile.description"),
                self.card_from_keys(translations, "mobileDevelopment.features.crossPlatform.title", "mobileDevelopment.features.crossPlatform.description"),
                self.card_from_keys(translations, "mobileDevelopment.features.cloud.title", "mobileDevelopment.features.cloud.description"),
                self.card_from_keys(translations, "mobileDevelopment.features.database.title", "mobileDevelopment.features.database.description"),
                self.card_from_keys(translations, "mobileDevelopment.careerPaths.ios.title", "mobileDevelopment.careerPaths.ios.description", "mobileDevelopment.careerPaths.ios.salary"),
                self.card_from_keys(translations, "mobileDevelopment.careerPaths.android.title", "mobileDevelopment.careerPaths.android.description", "mobileDevelopment.careerPaths.android.salary"),
                self.card_from_keys(translations, "mobileDevelopment.careerPaths.crossPlatform.title", "mobileDevelopment.careerPaths.crossPlatform.description", "mobileDevelopment.careerPaths.crossPlatform.salary"),
                self.card_from_keys(translations, "mobileDevelopment.careerPaths.architect.title", "mobileDevelopment.careerPaths.architect.description", "mobileDevelopment.careerPaths.architect.salary"),
            ],
            "media": [
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2481.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2512.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2476.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2487.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2574.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2662.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2562.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2577.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2674.jpg",
                "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2664.jpg",
            ],
            "documents": [],
        }

    def translated(self, translations, key):
        return {lang: safe_get(data, key) for lang, data in translations.items()}

    def card_from_keys(self, translations, title_key, description_key, extra_key=None):
        title = self.translated(translations, title_key)
        description = self.translated(translations, description_key)
        if extra_key:
            extra = self.translated(translations, extra_key)
            text = {
                lang: "\n".join(
                    part for part in [description[lang], extra[lang]] if part
                )
                for lang in ("ru", "en", "kg")
            }
        else:
            text = description
        return {"title": title, "text": text}

    def seed_page(self, config):
        page = Page.objects.get(path=config["path"])
        self.stdout.write(f"Processing {page.path}")

        if not self.apply:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: would replace sections/cards/media/documents for {page.path}"
                )
            )
            return

        page.title_ru = config["title"]["ru"]
        page.title_en = config["title"]["en"]
        page.title_kg = config["title"]["kg"]
        page.subtitle_ru = config["subtitle"]["ru"]
        page.subtitle_en = config["subtitle"]["en"]
        page.subtitle_kg = config["subtitle"]["kg"]
        page.body_ru = config["body"]["ru"]
        page.body_en = config["body"]["en"]
        page.body_kg = config["body"]["kg"]
        page.force_backend_render = True
        page.is_published = True
        page.data = {
            **(page.data or {}),
            "render_mode": "default",
            "badge": config["badge"]["ru"],
        }
        page.internal_notes = (
            "Страница пересобрана в структурированный CMS-формат из frontend переводов "
            "и внешних медиа Salymbekov.com. Контент теперь редактируется через секции, карточки, медиа и документы."
        )
        page.save()

        page.sections.all().delete()
        page.cards.all().delete()
        page.media_items.all().delete()
        page.documents.all().delete()
        page.links.all().delete()
        page.stats.all().delete()

        for order, section in enumerate(config["sections"], start=1):
            PageSection.objects.create(
                page=page,
                order=order,
                title_ru=section["title"]["ru"],
                title_en=section["title"]["en"],
                title_kg=section["title"]["kg"],
                body_ru=section["body"]["ru"],
                body_en=section["body"]["en"],
                body_kg=section["body"]["kg"],
            )

        for order, card in enumerate(config["cards"], start=1):
            PageCard.objects.create(
                page=page,
                order=order,
                title_ru=card["title"]["ru"],
                title_en=card["title"]["en"],
                title_kg=card["title"]["kg"],
                text_ru=card["text"]["ru"],
                text_en=card["text"]["en"],
                text_kg=card["text"]["kg"],
            )

        for order, url in enumerate(config["media"], start=1):
            media = PageMedia(
                page=page,
                order=order,
                media_type=PageMedia.TYPE_IMAGE,
                is_hero=order == 1,
                title_ru=f"{page.title_ru} — фото {order}",
                title_en=f"{page.title_en} — image {order}",
                title_kg=f"{page.title_kg} — сүрөт {order}",
                alt_text_ru=f"{page.title_ru} — фото {order}",
                alt_text_en=f"{page.title_en} — image {order}",
                alt_text_kg=f"{page.title_kg} — сүрөт {order}",
            )
            self.attach_remote_file(media, "file", url, fallback_external=True)
            media.save()

        for order, doc in enumerate(config["documents"], start=1):
            document = PageDocument(
                page=page,
                order=order,
                title_ru=doc["title"]["ru"],
                title_en=doc["title"]["en"],
                title_kg=doc["title"]["kg"],
            )
            self.attach_remote_file(document, "file", doc["url"], fallback_external=True)
            document.save()

        self.stdout.write(self.style.SUCCESS(f"Updated {page.path}"))

    def attach_remote_file(self, instance, field_name, url, fallback_external=False):
        if not self.download_assets:
            if fallback_external:
                instance.external_url = url
            return

        try:
            with urlopen(url, timeout=30) as response:
                content = response.read()
        except Exception as exc:
            self.stderr.write(self.style.WARNING(f"Failed to download {url}: {exc}"))
            if fallback_external:
                instance.external_url = url
            return

        path = urlsplit(url).path
        original_name = Path(path).name or "asset"
        stem = Path(original_name).stem or "asset"
        suffix = Path(original_name).suffix
        filename = f"{slugify(stem) or 'asset'}{suffix}"
        getattr(instance, field_name).save(filename, ContentFile(content), save=False)
